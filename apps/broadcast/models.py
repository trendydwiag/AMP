from django.db import models
from django.conf import settings
from utils.mixins import UUIDPrimaryKeyMixin, TimeStampedModel
from utils.choices import DayOfWeek, BroadcastStatus, ContentRating, ContentStatus, ContentPriority, ContentFormat


class Program(UUIDPrimaryKeyMixin, TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    short_description = models.CharField(max_length=500, blank=True, default='')
    full_description = models.TextField(blank=True, default='')
    thumbnail = models.ImageField(upload_to='broadcast/program/thumbnail/', blank=True, null=True)
    banner = models.ImageField(upload_to='broadcast/program/banner/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, default='')
    partner = models.ForeignKey(
        'platform.Partner', on_delete=models.CASCADE,
        null=True, blank=True, related_name='broadcast_programs',
        help_text="Partner yang memiliki program ini."
    )
    language = models.CharField(max_length=10, default='id')
    genre = models.CharField(max_length=100, blank=True, default='')
    target_audience = models.CharField(max_length=100, blank=True, default='')
    content_rating = models.CharField(
        max_length=5, choices=ContentRating.choices,
        default=ContentRating.GENERAL
    )
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    seo_title = models.CharField(max_length=200, blank=True, default='')
    seo_description = models.CharField(max_length=500, blank=True, default='')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='broadcast_programs_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='broadcast_programs_updated'
    )
    status = models.CharField(max_length=20, choices=ContentStatus.choices, default=ContentStatus.DRAFT)
    priority = models.CharField(max_length=10, choices=ContentPriority.choices, default=ContentPriority.NORMAL)
    content_format = models.CharField(max_length=15, choices=ContentFormat.choices, default=ContentFormat.RICH_TEXT)
    version = models.PositiveIntegerField(default=1)
    last_published_at = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(
        'content.Author', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='program_author'
    )
    tags_content = models.ManyToManyField('content.ContentTag', blank=True, related_name='programs_content')
    og_title = models.CharField(max_length=200, blank=True)
    og_description = models.CharField(max_length=500, blank=True)
    og_image = models.ImageField(upload_to='broadcast/program/og/', blank=True)
    twitter_card = models.CharField(max_length=20, default='summary_large_image')
    canonical_url = models.URLField(max_length=500, blank=True)
    robots = models.CharField(max_length=30, default='index,follow')
    schema_markup = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'
        ordering = ['title']

    def __str__(self) -> str:
        return self.title

    @property
    def hosts(self):
        return self.host_members.select_related('host')


class Host(UUIDPrimaryKeyMixin, TimeStampedModel):
    full_name = models.CharField(max_length=200)
    stage_name = models.CharField(max_length=200, blank=True, default='')
    nickname = models.CharField(max_length=100, blank=True, default='')
    biography = models.TextField(blank=True, default='')
    avatar = models.ImageField(upload_to='broadcast/host/avatar/', blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, default='')
    phone = models.CharField(max_length=50, blank=True, default='')
    instagram = models.CharField(max_length=200, blank=True, default='')
    youtube = models.CharField(max_length=200, blank=True, default='')
    spotify = models.CharField(max_length=200, blank=True, default='')
    facebook = models.CharField(max_length=200, blank=True, default='')
    website = models.URLField(max_length=500, blank=True, default='')
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Host'
        verbose_name_plural = 'Hosts'
        ordering = ['full_name']

    def __str__(self) -> str:
        return self.display_name

    @property
    def display_name(self) -> str:
        return self.stage_name or self.full_name

    @property
    def programs(self):
        return self.host_members.select_related('program')


class HostMember(UUIDPrimaryKeyMixin, TimeStampedModel):
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name='host_members')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='host_members')
    is_lead = models.BooleanField(default=False)
    joined_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Host Member'
        verbose_name_plural = 'Host Members'
        unique_together = ['host', 'program']

    def __str__(self) -> str:
        return f"{self.host.display_name} - {self.program.title}"


class Schedule(UUIDPrimaryKeyMixin, TimeStampedModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.CharField(max_length=3, choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    timezone = models.CharField(max_length=50, default='Asia/Jakarta')
    repeat_weekly = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'
        ordering = ['day_of_week', 'start_time']

    def __str__(self) -> str:
        return f"{self.program.title} - {self.get_day_of_week_display()} {self.start_time}"

    @property
    def duration_minutes(self) -> int:
        start = self.start_time
        end = self.end_time
        start_minutes = start.hour * 60 + start.minute
        end_minutes = end.hour * 60 + end.minute
        if end_minutes >= start_minutes:
            return end_minutes - start_minutes
        return (24 * 60 - start_minutes) + end_minutes

    @property
    def day_display(self) -> str:
        return self.get_day_of_week_display()


class BroadcastSession(UUIDPrimaryKeyMixin, TimeStampedModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='broadcast_sessions')
    schedule = models.ForeignKey(
        Schedule, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='sessions'
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=BroadcastStatus.choices,
        default=BroadcastStatus.SCHEDULED
    )

    class Meta:
        verbose_name = 'Broadcast Session'
        verbose_name_plural = 'Broadcast Sessions'
        ordering = ['-start_datetime']

    def __str__(self) -> str:
        return f"{self.program.title} - {self.get_status_display()} @ {self.start_datetime}"

    @property
    def is_live(self) -> bool:
        return self.status == BroadcastStatus.LIVE

    @property
    def is_finished(self) -> bool:
        return self.status == BroadcastStatus.FINISHED

    @property
    def duration_display(self) -> str:
        from django.utils import timezone
        end = self.end_datetime or timezone.now()
        delta = end - self.start_datetime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{hours}j {minutes}m"
        return f"{minutes}m {seconds}s"


class Episode(UUIDPrimaryKeyMixin, TimeStampedModel):
    broadcast_session = models.ForeignKey(
        BroadcastSession, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='episodes'
    )
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='episodes')
    episode_number = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, default='')
    cover_image = models.ImageField(upload_to='broadcast/episode/cover/', blank=True, null=True)
    recording_audio = models.FileField(upload_to='broadcast/episode/audio/', blank=True, null=True)
    recording_video = models.FileField(upload_to='broadcast/episode/video/', blank=True, null=True)
    published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ContentStatus.choices, default=ContentStatus.DRAFT)
    partner = models.ForeignKey(
        'platform.Partner', on_delete=models.CASCADE,
        null=True, blank=True, related_name='broadcast_episodes',
        help_text="Partner yang memiliki episode ini."
    )
    content_format = models.CharField(max_length=15, choices=ContentFormat.choices, default=ContentFormat.RICH_TEXT)
    transcript = models.TextField(blank=True, default='')
    version = models.PositiveIntegerField(default=1)
    last_published_at = models.DateTimeField(null=True, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    og_title = models.CharField(max_length=200, blank=True)
    og_description = models.CharField(max_length=500, blank=True)
    og_image = models.ImageField(upload_to='broadcast/episode/og/', blank=True)
    twitter_card = models.CharField(max_length=20, default='summary_large_image')
    canonical_url = models.URLField(max_length=500, blank=True)
    robots = models.CharField(max_length=30, default='index,follow')
    featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Episode'
        verbose_name_plural = 'Episodes'
        ordering = ['-publish_date']

    def __str__(self) -> str:
        return f"{self.program.title} - E{self.episode_number}: {self.title}"

    @property
    def is_published(self) -> bool:
        return self.status == ContentStatus.PUBLISHED and self.publish_date is not None


class GuestStar(UUIDPrimaryKeyMixin, TimeStampedModel):
    full_name = models.CharField(max_length=200)
    biography = models.TextField(blank=True, default='')
    photo = models.ImageField(upload_to='broadcast/guest/photo/', blank=True, null=True)
    organization = models.CharField(max_length=200, blank=True, default='')
    social_links = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = 'Guest Star'
        verbose_name_plural = 'Guest Stars'
        ordering = ['full_name']

    def __str__(self) -> str:
        return self.full_name


class EpisodeGuest(UUIDPrimaryKeyMixin, TimeStampedModel):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='episode_guests')
    guest = models.ForeignKey(GuestStar, on_delete=models.CASCADE, related_name='episode_guests')
    role = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        verbose_name = 'Episode Guest'
        verbose_name_plural = 'Episode Guests'
        unique_together = ['episode', 'guest']

    def __str__(self) -> str:
        return f"{self.guest.full_name} - {self.episode.title}"


class Playlist(UUIDPrimaryKeyMixin, TimeStampedModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='playlists')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'
        ordering = ['title']

    def __str__(self) -> str:
        return f"{self.program.title} - {self.title}"


class PlaylistItem(UUIDPrimaryKeyMixin, TimeStampedModel):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=300)
    artist = models.CharField(max_length=200, blank=True, default='')
    album = models.CharField(max_length=200, blank=True, default='')
    duration = models.PositiveIntegerField(default=0, help_text='Duration in seconds')
    sequence = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Playlist Item'
        verbose_name_plural = 'Playlist Items'
        ordering = ['sequence']

    def __str__(self) -> str:
        return f"{self.artist} - {self.title}" if self.artist else self.title


class Announcement(UUIDPrimaryKeyMixin, TimeStampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='broadcast/announcement/', blank=True, null=True)
    publish_start = models.DateTimeField()
    publish_end = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['-publish_start']

    def __str__(self) -> str:
        return self.title

    @property
    def is_current(self) -> bool:
        from django.utils import timezone
        now = timezone.now()
        if not self.active:
            return False
        if now < self.publish_start:
            return False
        if self.publish_end and now > self.publish_end:
            return False
        return True
