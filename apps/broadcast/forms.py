from django import forms
from django.utils.text import slugify
from .models import (
    Program, Host, HostMember, Schedule, BroadcastSession,
    Episode, GuestStar, EpisodeGuest, Playlist, PlaylistItem, Announcement
)
from utils.choices import DayOfWeek, BroadcastStatus, ContentRating


INPUT_ATTRS = {'class': 'form-input w-full'}
SELECT_ATTRS = {'class': 'form-select w-full'}
TEXTAREA_ATTRS = {'class': 'form-input w-full', 'rows': 3}
CHECKBOX_ATTRS = {'class': 'form-checkbox'}
FILE_ATTRS = {'class': 'form-input'}
TIME_ATTRS = {'class': 'form-input', 'type': 'time'}
DATETIME_ATTRS = {'class': 'form-input', 'type': 'datetime-local'}
DATE_ATTRS = {'class': 'form-input', 'type': 'date'}
NUMBER_ATTRS = {'class': 'form-input w-full', 'min': 0}


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = [
            'title', 'slug', 'short_description', 'full_description',
            'thumbnail', 'banner', 'category', 'language', 'genre',
            'target_audience', 'content_rating', 'featured', 'active',
            'seo_title', 'seo_description',
        ]
        widgets = {
            'title': forms.TextInput(attrs=INPUT_ATTRS),
            'slug': forms.TextInput(attrs=INPUT_ATTRS),
            'short_description': forms.TextInput(attrs=INPUT_ATTRS),
            'full_description': forms.Textarea(attrs=TEXTAREA_ATTRS),
            'thumbnail': forms.ClearableFileInput(attrs=FILE_ATTRS),
            'banner': forms.ClearableFileInput(attrs=FILE_ATTRS),
            'category': forms.TextInput(attrs=INPUT_ATTRS),
            'language': forms.TextInput(attrs=INPUT_ATTRS),
            'genre': forms.TextInput(attrs=INPUT_ATTRS),
            'target_audience': forms.TextInput(attrs=INPUT_ATTRS),
            'content_rating': forms.Select(attrs=SELECT_ATTRS, choices=ContentRating.choices),
            'featured': forms.CheckboxInput(attrs=CHECKBOX_ATTRS),
            'active': forms.CheckboxInput(attrs=CHECKBOX_ATTRS),
            'seo_title': forms.TextInput(attrs=INPUT_ATTRS),
            'seo_description': forms.Textarea(attrs={'class': 'form-input w-full', 'rows': 2}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            slug = slugify(self.cleaned_data.get('title', ''))
        return slug


class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = [
            'full_name', 'stage_name', 'nickname', 'biography', 'avatar',
            'email', 'phone', 'instagram', 'youtube', 'spotify',
            'facebook', 'website', 'active',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs=INPUT_ATTRS),
            'stage_name': forms.TextInput(attrs=INPUT_ATTRS),
            'nickname': forms.TextInput(attrs=INPUT_ATTRS),
            'biography': forms.Textarea(attrs=TEXTAREA_ATTRS),
            'avatar': forms.ClearableFileInput(attrs=FILE_ATTRS),
            'email': forms.EmailInput(attrs=INPUT_ATTRS),
            'phone': forms.TextInput(attrs=INPUT_ATTRS),
            'instagram': forms.TextInput(attrs=INPUT_ATTRS),
            'youtube': forms.TextInput(attrs=INPUT_ATTRS),
            'spotify': forms.TextInput(attrs=INPUT_ATTRS),
            'facebook': forms.TextInput(attrs=INPUT_ATTRS),
            'website': forms.URLInput(attrs=INPUT_ATTRS),
            'active': forms.CheckboxInput(attrs=CHECKBOX_ATTRS),
        }


class HostMemberForm(forms.ModelForm):
    class Meta:
        model = HostMember
        fields = ['host', 'program', 'is_lead', 'joined_date']
        widgets = {
            'host': forms.Select(attrs=SELECT_ATTRS),
            'program': forms.Select(attrs=SELECT_ATTRS),
            'is_lead': forms.CheckboxInput(attrs=CHECKBOX_ATTRS),
            'joined_date': forms.DateInput(attrs=DATE_ATTRS),
        }


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = [
            'program', 'day_of_week', 'start_time', 'end_time',
            'timezone', 'repeat_weekly', 'active',
        ]
        widgets = {
            'program': forms.Select(attrs=SELECT_ATTRS),
            'day_of_week': forms.Select(attrs=SELECT_ATTRS, choices=DayOfWeek.choices),
            'start_time': forms.TimeInput(attrs=TIME_ATTRS),
            'end_time': forms.TimeInput(attrs=TIME_ATTRS),
            'timezone': forms.TextInput(attrs=INPUT_ATTRS),
            'repeat_weekly': forms.CheckboxInput(attrs=CHECKBOX_ATTRS),
            'active': forms.CheckboxInput(attrs=CHECKBOX_ATTRS),
        }


class BroadcastSessionForm(forms.ModelForm):
    class Meta:
        model = BroadcastSession
        fields = ['program', 'schedule', 'start_datetime', 'end_datetime', 'status']
        widgets = {
            'program': forms.Select(attrs=SELECT_ATTRS),
            'schedule': forms.Select(attrs=SELECT_ATTRS),
            'start_datetime': forms.DateTimeInput(attrs=DATETIME_ATTRS),
            'end_datetime': forms.DateTimeInput(attrs=DATETIME_ATTRS),
            'status': forms.Select(attrs=SELECT_ATTRS, choices=BroadcastStatus.choices),
        }


class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = [
            'broadcast_session', 'program', 'episode_number', 'title',
            'description', 'cover_image', 'recording_audio', 'recording_video',
            'published', 'publish_date',
        ]
        widgets = {
            'broadcast_session': forms.Select(attrs=SELECT_ATTRS),
            'program': forms.Select(attrs=SELECT_ATTRS),
            'episode_number': forms.NumberInput(attrs=NUMBER_ATTRS),
            'title': forms.TextInput(attrs=INPUT_ATTRS),
            'description': forms.Textarea(attrs=TEXTAREA_ATTRS),
            'cover_image': forms.ClearableFileInput(attrs=FILE_ATTRS),
            'recording_audio': forms.ClearableFileInput(attrs=FILE_ATTRS),
            'recording_video': forms.ClearableFileInput(attrs=FILE_ATTRS),
            'published': forms.CheckboxInput(attrs=CHECKBOX_ATTRS),
            'publish_date': forms.DateTimeInput(attrs=DATETIME_ATTRS),
        }


class GuestStarForm(forms.ModelForm):
    class Meta:
        model = GuestStar
        fields = ['full_name', 'biography', 'photo', 'organization', 'social_links']
        widgets = {
            'full_name': forms.TextInput(attrs=INPUT_ATTRS),
            'biography': forms.Textarea(attrs=TEXTAREA_ATTRS),
            'photo': forms.ClearableFileInput(attrs=FILE_ATTRS),
            'organization': forms.TextInput(attrs=INPUT_ATTRS),
            'social_links': forms.Textarea(attrs={'class': 'form-input w-full', 'rows': 3, 'placeholder': '{"instagram": "@handle"}'}),
        }


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['program', 'title', 'description', 'active']
        widgets = {
            'program': forms.Select(attrs=SELECT_ATTRS),
            'title': forms.TextInput(attrs=INPUT_ATTRS),
            'description': forms.Textarea(attrs=TEXTAREA_ATTRS),
            'active': forms.CheckboxInput(attrs=CHECKBOX_ATTRS),
        }


class PlaylistItemForm(forms.ModelForm):
    class Meta:
        model = PlaylistItem
        fields = ['playlist', 'title', 'artist', 'album', 'duration', 'sequence']
        widgets = {
            'playlist': forms.Select(attrs=SELECT_ATTRS),
            'title': forms.TextInput(attrs=INPUT_ATTRS),
            'artist': forms.TextInput(attrs=INPUT_ATTRS),
            'album': forms.TextInput(attrs=INPUT_ATTRS),
            'duration': forms.NumberInput(attrs=NUMBER_ATTRS),
            'sequence': forms.NumberInput(attrs=NUMBER_ATTRS),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'image', 'publish_start', 'publish_end', 'active']
        widgets = {
            'title': forms.TextInput(attrs=INPUT_ATTRS),
            'content': forms.Textarea(attrs=TEXTAREA_ATTRS),
            'image': forms.ClearableFileInput(attrs=FILE_ATTRS),
            'publish_start': forms.DateTimeInput(attrs=DATETIME_ATTRS),
            'publish_end': forms.DateTimeInput(attrs=DATETIME_ATTRS),
            'active': forms.CheckboxInput(attrs=CHECKBOX_ATTRS),
        }


class BroadcastSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input w-full',
            'placeholder': 'Cari program, host, atau episode...',
        })
    )
