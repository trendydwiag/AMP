# Sprint 4.2 — Media Pipeline Engine

**Tanggal:** 17 Juli 2026
**Tipe:** Backend Architecture — tidak ada perubahan UI
**Objective:** Bangun fondasi pipeline upload media yang bisa digunakan oleh semua modul (lagu, podcast, jingle, iklan, sponsor, sound effect, voice insert, cover, thumbnail)

---

## Architecture

### Pipeline Flow

```
MediaFileService.upload_file()
        │
        ▼
MediaPipelineService.process(file_obj, PipelineContext)
        │
        ├─ Stage 1: validate()
        │    ├─ Extension whitelist check
        │    ├─ File size vs MediaSettings.max_file_size_mb
        │    ├─ MIME type consistency check
        │    └─ Duplicate filename warning (non-blocking)
        │
        ├─ Stage 2: extract_metadata()
        │    ├─ filename, extension, mime_type, size — always
        │    └─ duration, bitrate, title, artist, album — audio/video via mutagen
        │
        ├─ Stage 3: _create_record() [DB save, status=PROCESSING]
        │    └─ Creates MediaFile with pipeline_status='PROCESSING'
        │
        ├─ Stage 4: generate_waveform() ← STUB
        ├─ Stage 5: analyze_audio()     ← STUB
        ├─ Stage 6: generate_preview()  ← STUB
        │
        ├─ Stage 7: Mark READY [pipeline_status='READY', processed_at=now()]
        │
        └─ Stage 8: dispatch_event()
             ├─ EVENT_MEDIA_UPLOADED
             └─ EVENT_MEDIA_PROCESSED

If any stage raises → _mark_failed() → EVENT_MEDIA_FAILED
```

### Layer Diagram

```
View (MediaUploadView)
  → MediaFileService.upload_file()       ← unchanged interface
      → MediaPipelineService.process()   ← NEW pipeline orchestrator
          → validate()                   ← uses validators.py
          → extract_metadata()           ← uses mutagen
          → _create_record()             ← saves to DB
          → generate_waveform/analyze/preview (STUBS)
          → dispatch_event()             ← events.py dispatcher
```

---

## New Files

### `apps/media_manager/pipeline.py`
MediaPipelineService — orchestrates all upload stages.

**Classes:**
- `PipelineError` / `PipelineValidationError` / `PipelineMetadataError` / `PipelineSaveError` — exception hierarchy
- `MediaMetadata` — dataclass: filename, extension, mime_type, size, duration, bitrate, title, artist, album
- `PipelineContext` — dataclass: user, title, folder_id, alt_text, caption, is_public, tag_ids, partner, extra
- `PipelineResult` — dataclass: success, media_file, metadata, error, stage
- `MediaPipelineService` — orchestrator with 8 stage methods

### `apps/media_manager/storage.py`
Storage abstraction layer.

**Classes:**
- `BaseStorageBackend` (ABC) — interface: save(), delete(), url(), exists(), backend_name
- `LocalStorageBackend` — wraps Django `default_storage` (ACTIVE)
- `S3StorageBackend` — STUB (requires boto3 + django-storages)
- `CloudflareR2Backend` — STUB (S3-compatible with R2 endpoint)
- `MinIOBackend` — STUB (S3-compatible with MinIO endpoint)

**Factory:**
- `get_storage_backend(backend_name=None)` — resolves backend from arg → MediaSettings → 'local'
- `register_storage_backend(name, cls)` — register custom backends in AppConfig.ready()

### `apps/media_manager/events.py`
Lightweight pub/sub event dispatcher.

**Constants:**
- `EVENT_MEDIA_UPLOADED = 'media.uploaded'`
- `EVENT_MEDIA_PROCESSED = 'media.processed'`
- `EVENT_MEDIA_DELETED = 'media.deleted'`
- `EVENT_MEDIA_UPDATED = 'media.updated'`
- `EVENT_MEDIA_FAILED = 'media.failed'`
- `EVENT_MEDIA_ARCHIVED = 'media.archived'`

**Classes:**
- `MediaEvent` — dataclass: name, media_file, timestamp, metadata
- `MediaEventDispatcher` — class-level registry; methods: register(), on() (decorator), dispatch(), clear()

---

## Modified Files

### `apps/media_manager/models.py`
Added `PipelineStatus` TextChoices enum and 9 new fields to `MediaFile`:

| Field | Type | Default | Description |
|---|---|---|---|
| `pipeline_status` | CharField (Choice) | READY | UPLOADING/PROCESSING/READY/FAILED/ARCHIVED |
| `processed_at` | DateTimeField | null | When pipeline completed |
| `storage_backend` | CharField | 'local' | Backend used for storage |
| `duration` | FloatField | null | Audio/video duration in seconds |
| `bitrate` | IntegerField | null | Bitrate in kbps |
| `audio_title` | CharField | '' | ID3/Vorbis title tag |
| `audio_artist` | CharField | '' | ID3/Vorbis artist tag |
| `audio_album` | CharField | '' | ID3/Vorbis album tag |
| `pipeline_error` | TextField | '' | Error message if FAILED |

New model properties: `duration_formatted` (MM:SS), `pipeline_status_badge` (CSS classes)

### `apps/media_manager/services.py`
`MediaFileService.upload_file()` — refactored to use `MediaPipelineService` internally.
- Interface unchanged: same parameters, same return value (MediaFile instance)
- Raises `ValueError` if pipeline fails (was: silent save without validation)
- `_detect_file_type()` helper removed (now in pipeline.py)
- Added optional `partner=None` parameter

### `apps/media_manager/views.py`
Added `MediaInspectorView` — paginated (50/page) list of all MediaFile records with pipeline metadata, filterable by status/type/query.

### `apps/media_manager/urls.py`
Added: `path('inspector/', MediaInspectorView, name='inspector')` → `/media/inspector/`

### `templates/media_manager/inspector.html`
Media Inspector page extending `amp_studio/base.html`:
- Status summary cards (count per pipeline_status + total)
- Alert banners for FAILED and PROCESSING files
- Filter bar (search, status dropdown, type dropdown)
- Table: filename+tags, file_type, pipeline_status, duration, bitrate, size, storage, uploaded_by, processed_at
- Pipeline lifecycle legend
- Pagination

### `requirements/base.txt`
Added: `mutagen>=1.47.0`

---

## New Migration

`apps/media_manager/migrations/0003_sprint42_pipeline_fields.py`
- Adds 9 pipeline fields to `mediafile` table
- All nullable or have defaults → zero-downtime safe
- Existing records get `pipeline_status='READY'` (correct — they're already usable)

---

## Task 10: Audit — Uploads NOT Going Through Pipeline

The following uploads currently bypass `MediaPipelineService`:

| Location | Field | Current Behavior |
|---|---|---|
| `apps/broadcast/models.py` | `Episode.recording_audio` | Direct FileField — no validation, no metadata |
| `apps/broadcast/models.py` | `Episode.recording_video` | Direct FileField — no validation, no metadata |
| `apps/podcast/models.py` | `PodcastEpisode.audio_file` | Direct FileField — no validation, no metadata |
| `apps/settings/models.py` | `SiteSettings.logo` / `SiteSettings.favicon` | ImageField — no pipeline |
| `apps/users/models.py` | `UserProfile.avatar` | ImageField — no pipeline |
| `apps/broadcast/models.py` | `Host.avatar` | ImageField — no pipeline |

**These are NOT changed in this sprint** (per sprint rules: do not change business logic).
They are documented here for future sprints that will wire them through the pipeline.

---

## Known Limitations

1. **Stages 4–6 are stubs** — `generate_waveform()`, `analyze_audio()`, `generate_preview()` always log DEBUG and return None. Full implementation requires ffmpeg / pydub / pyloudnorm (future sprint).

2. **No async** — Pipeline runs synchronously in the request cycle. For large files, this blocks the response. Move to Celery task when async infra is ready.

3. **storage_backend field** — Always 'local' today. Will reflect the actual backend name when S3/R2/MinIO are implemented.

4. **Existing MediaFile records** — Rows uploaded before Sprint 4.2 have `pipeline_status='READY'` (correct default), `duration=null`, `bitrate=null`. They will NOT have metadata auto-backfilled. A future management command should do this.

5. **Duplicate filename** — Currently a warning only. Future: enforce uniqueness per partner.

---

## Future Enhancements

| Enhancement | Effort | Priority |
|---|---|---|
| Celery task for stages 4–6 | Medium | High when file volume grows |
| S3 storage backend | Medium | When Replit Object Storage or AWS S3 is configured |
| `generate_waveform()` via pydub | Medium | For player visualiser |
| `analyze_audio()` via pyloudnorm | Medium | For broadcast loudness compliance |
| Metadata backfill management command | Small | Low (existing files) |
| Wire broadcast/podcast audio through pipeline | Medium | Medium (next sprint) |
| Per-partner upload limits (MB/month) | Medium | Medium |

---

## Compatibility

- **Breaking changes:** None — `MediaFileService.upload_file()` interface unchanged
- **Database:** Migration 0003 adds columns with defaults → backward compatible
- **Templates:** No changes to existing templates
- **Upload flow from UI:** Unchanged — `MediaUploadView` still calls `service.upload_file()`
- **Existing MediaFile records:** Unaffected — all default to `pipeline_status='READY'`
