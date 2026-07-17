"""
Media Pipeline Engine
~~~~~~~~~~~~~~~~~~~~~~
MediaPipelineService orchestrates all upload processing stages:

    validate → extract_metadata → save → generate_waveform (stub)
             → analyze_audio (stub) → generate_preview (stub)
             → dispatch_event

All stages are synchronous today but structured so each can be extracted
into a Celery task without changing the pipeline interface.

Usage:
    pipeline = MediaPipelineService()
    result = pipeline.process(file_obj, context)
    if result.success:
        media = result.media_file
    else:
        print(result.error)
"""
from __future__ import annotations

import logging
import mimetypes
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from django.db import transaction
from django.utils import timezone

from .events import MediaEventDispatcher, EVENT_MEDIA_UPLOADED, EVENT_MEDIA_PROCESSED, EVENT_MEDIA_FAILED
from .storage import get_storage_backend

logger = logging.getLogger(__name__)


# ── Exceptions ────────────────────────────────────────────────────────────────
class PipelineError(Exception):
    """Base class for all pipeline errors."""

class PipelineValidationError(PipelineError):
    """Raised when the file fails validation."""

class PipelineMetadataError(PipelineError):
    """Raised when metadata extraction fails unrecoverably."""

class PipelineSaveError(PipelineError):
    """Raised when persisting the record to the database fails."""


# ── Metadata dataclass ────────────────────────────────────────────────────────
@dataclass
class MediaMetadata:
    """
    Extracted metadata from the uploaded file.
    All fields except filename/extension/mime_type/size may be None
    if the file type doesn't carry the relevant information.
    """
    filename: str           # original filename (e.g. "jingle_pagi.mp3")
    extension: str          # lowercase without dot (e.g. "mp3")
    mime_type: str          # detected MIME type (e.g. "audio/mpeg")
    size: int               # bytes
    duration: float | None = None    # seconds (audio/video only)
    bitrate: int | None = None       # kbps (audio only)
    title: str | None = None         # ID3/Vorbis tag or filename stem
    artist: str | None = None        # ID3/Vorbis tag
    album: str | None = None         # ID3/Vorbis tag

    @property
    def duration_formatted(self) -> str:
        if self.duration is None:
            return '—'
        minutes = int(self.duration // 60)
        seconds = int(self.duration % 60)
        return f'{minutes:02d}:{seconds:02d}'

    @property
    def size_formatted(self) -> str:
        size = self.size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f'{size:.1f} {unit}'
            size /= 1024.0
        return f'{size:.1f} TB'


# ── Pipeline context ──────────────────────────────────────────────────────────
@dataclass
class PipelineContext:
    """
    All caller-supplied parameters for a single pipeline run.
    Pass this to MediaPipelineService.process().
    """
    user: Any                       # authenticated User instance
    title: str = ''
    folder_id: Any = None           # UUID or None
    alt_text: str = ''
    caption: str = ''
    is_public: bool = True
    tag_ids: list | None = None
    partner: Any = None             # Partner instance or None
    extra: dict = field(default_factory=dict)


# ── Pipeline result ───────────────────────────────────────────────────────────
@dataclass
class PipelineResult:
    """Returned by MediaPipelineService.process()."""
    success: bool
    media_file: Any = None          # MediaFile instance if success
    metadata: MediaMetadata | None = None
    error: str = ''
    stage: str = ''                 # Which stage failed (if not success)


# ── Pipeline service ──────────────────────────────────────────────────────────
class MediaPipelineService:
    """
    Orchestrates the full upload pipeline for a single file.

    Design principles:
    - Each stage is a separate method → easy to mock / override in tests
    - Stages communicate via return values, not shared state
    - Failures set pipeline_status=FAILED and always dispatch EVENT_MEDIA_FAILED
    - Background-ready: wrap process() in a Celery task to go async
    """

    # ── Public entry point ────────────────────────────────────────────────────
    def process(self, file_obj: Any, context: PipelineContext) -> PipelineResult:
        """
        Run the full pipeline for file_obj.

        Stages:
            1. validate          — check extension, size, duplicates
            2. extract_metadata  — read filename, mime, tags, duration, bitrate
            3. save              — persist MediaFile to DB (status=PROCESSING)
            4. generate_waveform — STUB (future: waveform image for player)
            5. analyze_audio     — STUB (future: loudness, BPM analysis)
            6. generate_preview  — STUB (future: transcoded preview clip)
            7. mark READY        — set pipeline_status=READY, processed_at=now
            8. dispatch_event    — fire EVENT_MEDIA_UPLOADED + EVENT_MEDIA_PROCESSED

        Returns:
            PipelineResult with success=True and the saved MediaFile, or
            PipelineResult with success=False and an error description.
        """
        media_file = None
        metadata = None

        try:
            # Stage 1: validate
            self.validate(file_obj, context)

            # Stage 2: extract metadata
            metadata = self.extract_metadata(file_obj)
            if not context.title:
                context.title = metadata.title or os.path.splitext(metadata.filename)[0]

            # Stage 3: save to DB (status=PROCESSING)
            with transaction.atomic():
                media_file = self._create_record(file_obj, metadata, context)

            # Stages 4–6: post-save processing (stubs — won't raise)
            self.generate_waveform(media_file)
            self.analyze_audio(media_file)
            self.generate_preview(media_file)

            # Stage 7: mark READY
            with transaction.atomic():
                media_file.pipeline_status = 'READY'
                media_file.processed_at = timezone.now()
                media_file.save(update_fields=['pipeline_status', 'processed_at'])

            # Stage 8: dispatch events
            self.dispatch_event(EVENT_MEDIA_UPLOADED, media_file, {'metadata': metadata})
            self.dispatch_event(EVENT_MEDIA_PROCESSED, media_file, {'metadata': metadata})

            logger.info(
                "Pipeline complete: %r | %s | %s | %s",
                media_file.title,
                metadata.mime_type,
                metadata.size_formatted,
                metadata.duration_formatted,
            )
            return PipelineResult(success=True, media_file=media_file, metadata=metadata)

        except PipelineValidationError as exc:
            logger.warning("Pipeline validation failed for %r: %s", getattr(file_obj, 'name', '?'), exc)
            if media_file:
                self._mark_failed(media_file, str(exc))
            return PipelineResult(success=False, error=str(exc), stage='validate', metadata=metadata)

        except PipelineMetadataError as exc:
            logger.warning("Pipeline metadata error for %r: %s", getattr(file_obj, 'name', '?'), exc)
            if media_file:
                self._mark_failed(media_file, str(exc))
            return PipelineResult(success=False, error=str(exc), stage='extract_metadata', metadata=metadata)

        except PipelineSaveError as exc:
            logger.error("Pipeline save error for %r: %s", getattr(file_obj, 'name', '?'), exc)
            return PipelineResult(success=False, error=str(exc), stage='save', metadata=metadata)

        except Exception as exc:
            logger.exception("Unexpected pipeline error for %r", getattr(file_obj, 'name', '?'))
            if media_file:
                self._mark_failed(media_file, str(exc))
            return PipelineResult(success=False, error=f'Kesalahan tidak terduga: {exc}', stage='unknown', metadata=metadata)

    # ── Stage 1: Validate ─────────────────────────────────────────────────────
    def validate(self, file_obj: Any, context: PipelineContext) -> None:
        """
        Check that the file passes all validation rules.
        Raises PipelineValidationError if any check fails.

        Rules (in order):
            1. Extension must be in the allowed list
            2. File size must not exceed the configured maximum
            3. MIME type must match the extension category
            4. Duplicate filename check (warn, not block)
        """
        from apps.media_manager.validators import ALLOWED_EXTENSIONS

        original_name = getattr(file_obj, 'name', '')
        ext = os.path.splitext(original_name)[1].lower().lstrip('.')
        size = getattr(file_obj, 'size', 0)

        # Rule 1: Extension whitelist
        all_exts = set()
        for exts in ALLOWED_EXTENSIONS.values():
            all_exts.update(exts)
        if ext and ext not in all_exts:
            raise PipelineValidationError(
                f'Ekstensi file tidak diizinkan: .{ext}. '
                f'Ekstensi yang diizinkan: {", ".join(sorted(all_exts))}'
            )

        # Rule 2: File size
        max_mb = self._get_max_size_mb()
        if size > max_mb * 1024 * 1024:
            raise PipelineValidationError(
                f'Ukuran file ({size / (1024 * 1024):.1f} MB) melebihi batas '
                f'maksimum ({max_mb} MB).'
            )

        # Rule 3: MIME type vs extension consistency
        guessed_mime = mimetypes.guess_type(original_name)[0]
        if guessed_mime and ext in all_exts:
            ext_category = self._extension_category(ext)
            mime_category = guessed_mime.split('/')[0]
            if ext_category and mime_category and ext_category != mime_category and ext != 'ogg':
                raise PipelineValidationError(
                    f'Tipe MIME ({guessed_mime}) tidak konsisten dengan ekstensi .{ext}'
                )

        # Rule 4: Duplicate filename (warn only — not a hard block)
        from apps.media_manager.models import MediaFile
        if MediaFile.objects.filter(original_filename=original_name).exists():
            logger.warning(
                "Duplicate filename detected: %r (allowing upload, filename not unique)",
                original_name,
            )

    # ── Stage 2: Extract metadata ─────────────────────────────────────────────
    def extract_metadata(self, file_obj: Any) -> MediaMetadata:
        """
        Extract file metadata. For audio/video, reads tags and duration via mutagen.
        Gracefully falls back if mutagen cannot parse the file.

        Populates:
            filename, extension, mime_type, size — always
            duration, bitrate, title, artist, album — audio/video only
        """
        original_name = getattr(file_obj, 'name', '')
        ext = os.path.splitext(original_name)[1].lower().lstrip('.')
        size = getattr(file_obj, 'size', 0)
        mime_type = mimetypes.guess_type(original_name)[0] or 'application/octet-stream'

        metadata = MediaMetadata(
            filename=original_name,
            extension=ext,
            mime_type=mime_type,
            size=size,
        )

        # Only attempt audio/video metadata extraction
        is_audio = mime_type.startswith('audio/') or ext in {'mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a'}
        is_video = mime_type.startswith('video/')
        if not (is_audio or is_video):
            return metadata

        try:
            import mutagen
            # mutagen.File works with file-like objects
            file_obj.seek(0)
            audio = mutagen.File(file_obj, easy=True)
            file_obj.seek(0)  # reset for Django's save machinery

            if audio is not None:
                # Duration
                info = getattr(audio, 'info', None)
                if info and hasattr(info, 'length'):
                    metadata.duration = round(float(info.length), 2)

                # Bitrate — present on MP3, FLAC, AAC info objects
                if info and hasattr(info, 'bitrate'):
                    metadata.bitrate = int(info.bitrate // 1000) if info.bitrate else None

                # ID3 / EasyID3 tags (easy=True normalises them)
                tags = dict(audio.tags or {})
                metadata.title = self._first_tag(tags, 'title') or os.path.splitext(original_name)[0]
                metadata.artist = self._first_tag(tags, 'artist')
                metadata.album = self._first_tag(tags, 'album')

        except Exception as exc:
            # Metadata extraction is best-effort — never block the upload
            logger.warning("mutagen could not parse %r: %s", original_name, exc)

        return metadata

    # ── Stage 3 (internal): Save record ───────────────────────────────────────
    def _create_record(self, file_obj: Any, metadata: MediaMetadata, context: PipelineContext) -> Any:
        """Create the MediaFile DB record. Sets status=PROCESSING during creation."""
        from apps.media_manager.models import MediaFile

        storage = get_storage_backend()

        try:
            media = MediaFile(
                title=context.title or metadata.title or os.path.splitext(metadata.filename)[0],
                file=file_obj,
                original_filename=metadata.filename,
                file_type=self._detect_file_type(metadata.mime_type, metadata.extension),
                mime_type=metadata.mime_type,
                file_size=metadata.size,
                folder_id=context.folder_id,
                uploaded_by=context.user,
                is_public=context.is_public,
                alt_text=context.alt_text,
                caption=context.caption,
                # Pipeline fields
                pipeline_status='PROCESSING',
                storage_backend=storage.backend_name,
                duration=metadata.duration,
                bitrate=metadata.bitrate,
                audio_title=metadata.title or '',
                audio_artist=metadata.artist or '',
                audio_album=metadata.album or '',
            )
            if context.partner:
                media.partner = context.partner
            media.save()

            if context.tag_ids:
                media.tags.set(context.tag_ids)

            return media

        except Exception as exc:
            raise PipelineSaveError(f'Gagal menyimpan file ke database: {exc}') from exc

    # ── Stage 4: Generate waveform (STUB) ─────────────────────────────────────
    def generate_waveform(self, media_file: Any) -> None:
        """
        STUB — Generate a waveform image for the audio player visualiser.
        Future implementation: use pydub / audiowaveform to produce a PNG/SVG.
        Store result path in MediaFile.waveform_image (field to be added in future sprint).
        """
        logger.debug("generate_waveform: STUB for %r", getattr(media_file, 'title', '?'))

    # ── Stage 5: Analyze audio (STUB) ─────────────────────────────────────────
    def analyze_audio(self, media_file: Any) -> None:
        """
        STUB — Analyze audio characteristics.
        Future implementation: use pyloudnorm for LUFS loudness, BPM detection.
        Store results in MediaFile.loudness_lufs, MediaFile.bpm (fields to be added).
        """
        logger.debug("analyze_audio: STUB for %r", getattr(media_file, 'title', '?'))

    # ── Stage 6: Generate preview (STUB) ─────────────────────────────────────
    def generate_preview(self, media_file: Any) -> None:
        """
        STUB — Transcode a preview/clip.
        Future implementation: use ffmpeg to produce a 30-second MP3 preview.
        Store result path in MediaFile.preview_file (field to be added).
        """
        logger.debug("generate_preview: STUB for %r", getattr(media_file, 'title', '?'))

    # ── Stage 7 (internal): Mark failed ──────────────────────────────────────
    def _mark_failed(self, media_file: Any, error_message: str) -> None:
        """Set status=FAILED on a partially created MediaFile."""
        try:
            media_file.pipeline_status = 'FAILED'
            media_file.pipeline_error = error_message[:1000]
            media_file.save(update_fields=['pipeline_status', 'pipeline_error'])
            self.dispatch_event(EVENT_MEDIA_FAILED, media_file, {'error': error_message})
        except Exception as exc:
            logger.error("Could not mark media_file as FAILED: %s", exc)

    # ── Stage 8: Dispatch event ───────────────────────────────────────────────
    def dispatch_event(self, event_name: str, media_file: Any, metadata: dict | None = None) -> None:
        """Dispatch a lifecycle event to all registered handlers."""
        MediaEventDispatcher.dispatch(event_name, media_file, metadata)

    # ── Helpers ───────────────────────────────────────────────────────────────
    @staticmethod
    def _get_max_size_mb() -> int:
        try:
            from apps.settings.models import MediaSettings
            return MediaSettings.load().max_file_size_mb or 100
        except Exception:
            return 100

    @staticmethod
    def _detect_file_type(mime_type: str, ext: str) -> str:
        if mime_type and mime_type.startswith('image/'):
            return 'IMAGE'
        if mime_type and mime_type.startswith('video/'):
            return 'VIDEO'
        if mime_type and mime_type.startswith('audio/'):
            return 'AUDIO'
        doc_exts = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.csv', '.rtf'}
        if f'.{ext}' in doc_exts:
            return 'DOCUMENT'
        return 'OTHER'

    @staticmethod
    def _extension_category(ext: str) -> str | None:
        """Return 'image', 'audio', 'video', or None for document/other."""
        image_exts = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp', 'ico'}
        audio_exts = {'mp3', 'wav', 'flac', 'aac', 'm4a'}
        video_exts = {'mp4', 'webm', 'avi', 'mov', 'mkv'}
        if ext in image_exts:
            return 'image'
        if ext in audio_exts:
            return 'audio'
        if ext in video_exts:
            return 'video'
        return None

    @staticmethod
    def _first_tag(tags: dict, key: str) -> str | None:
        """EasyID3 returns lists — grab the first non-empty value."""
        val = tags.get(key)
        if isinstance(val, list) and val:
            return str(val[0]).strip() or None
        if isinstance(val, str):
            return val.strip() or None
        return None
