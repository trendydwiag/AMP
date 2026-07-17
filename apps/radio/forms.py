from django import forms
from .models import RadioStation, RadioProvider


class RadioStationForm(forms.ModelForm):
    class Meta:
        model = RadioStation
        fields = [
            'station_name', 'station_description', 'logo', 'banner',
            'timezone', 'country', 'language', 'genre', 'website',
            'default_volume', 'autoplay', 'sticky_player', 'is_active'
        ]
        widgets = {
            'station_name': forms.TextInput(attrs={'class': 'form-input'}),
            'station_description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'banner': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'timezone': forms.TextInput(attrs={'class': 'form-input'}),
            'country': forms.TextInput(attrs={'class': 'form-input'}),
            'language': forms.TextInput(attrs={'class': 'form-input'}),
            'genre': forms.TextInput(attrs={'class': 'form-input'}),
            'website': forms.URLInput(attrs={'class': 'form-input'}),
            'default_volume': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 100}),
            'autoplay': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'sticky_player': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class RadioProviderForm(forms.ModelForm):
    class Meta:
        model = RadioProvider
        fields = [
            'station', 'provider_name', 'provider_type',
            'api_url', 'stream_url', 'backup_stream_url',
            'metadata_url', 'listener_url', 'healthcheck_url',
            'username', 'password', 'timeout', 'active', 'metadata_format'
        ]
        widgets = {
            'station': forms.Select(attrs={'class': 'form-select'}),
            'provider_name': forms.TextInput(attrs={'class': 'form-input'}),
            'provider_type': forms.Select(attrs={'class': 'form-select'}),
            'api_url': forms.URLInput(attrs={'class': 'form-input'}),
            'stream_url': forms.URLInput(attrs={'class': 'form-input'}),
            'backup_stream_url': forms.URLInput(attrs={'class': 'form-input'}),
            'metadata_url': forms.URLInput(attrs={'class': 'form-input'}),
            'listener_url': forms.URLInput(attrs={'class': 'form-input'}),
            'healthcheck_url': forms.URLInput(attrs={'class': 'form-input'}),
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password': forms.PasswordInput(attrs={'class': 'form-input'}, render_value=True),
            'timeout': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 60}),
            'active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'metadata_format': forms.Select(attrs={'class': 'form-select'}),
        }
