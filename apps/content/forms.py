from django import forms
from .models import (
    ContentCategory, ContentTag, Author, SEOModel,
    ContentVersion, PublishingQueue, ContentHighlight
)


class ContentCategoryForm(forms.ModelForm):
    class Meta:
        model = ContentCategory
        fields = ['name', 'slug', 'description', 'content_type', 'parent', 'icon', 'color', 'active', 'display_order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'content_type': forms.Select(attrs={'class': 'form-select'}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
            'icon': forms.TextInput(attrs={'class': 'form-input'}),
            'color': forms.TextInput(attrs={'class': 'form-input', 'type': 'color'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Nama kategori wajib diisi.")
        return name


class ContentTagForm(forms.ModelForm):
    class Meta:
        model = ContentTag
        fields = ['name', 'slug', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'color': forms.TextInput(attrs={'class': 'form-input', 'type': 'color'}),
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['user', 'name', 'slug', 'bio', 'avatar', 'email', 'website', 'social_links', 'active']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'website': forms.URLInput(attrs={'class': 'form-input'}),
        }


class SEOForm(forms.ModelForm):
    class Meta:
        model = SEOModel
        fields = [
            'title', 'description', 'keywords',
            'og_title', 'og_description', 'og_image', 'og_type',
            'twitter_card', 'twitter_title', 'twitter_description', 'twitter_image',
            'canonical_url', 'robots', 'schema_markup',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'maxlength': 200}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'maxlength': 500}),
            'keywords': forms.TextInput(attrs={'class': 'form-input'}),
            'og_title': forms.TextInput(attrs={'class': 'form-input'}),
            'og_description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'og_type': forms.Select(attrs={'class': 'form-select'}),
            'twitter_card': forms.Select(attrs={'class': 'form-select'}),
            'twitter_title': forms.TextInput(attrs={'class': 'form-input'}),
            'twitter_description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'canonical_url': forms.URLInput(attrs={'class': 'form-input'}),
            'robots': forms.Select(attrs={'class': 'form-select'}),
        }


class ContentVersionForm(forms.ModelForm):
    class Meta:
        model = ContentVersion
        fields = ['change_summary']
        widgets = {
            'change_summary': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
        }


class PublishingQueueForm(forms.ModelForm):
    class Meta:
        model = PublishingQueue
        fields = ['content_type', 'content_id', 'scheduled_at']
        widgets = {
            'content_type': forms.Select(attrs={'class': 'form-select'}),
            'content_id': forms.TextInput(attrs={'class': 'form-input'}),
            'scheduled_at': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
        }


class ContentHighlightForm(forms.ModelForm):
    class Meta:
        model = ContentHighlight
        fields = [
            'highlight_type', 'content_type', 'content_id',
            'title_override', 'description_override', 'image_override',
            'display_order', 'active', 'start_date', 'end_date',
        ]
        widgets = {
            'highlight_type': forms.Select(attrs={'class': 'form-select'}),
            'content_type': forms.Select(attrs={'class': 'form-select'}),
            'content_id': forms.TextInput(attrs={'class': 'form-input'}),
            'title_override': forms.TextInput(attrs={'class': 'form-input'}),
            'description_override': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
        }


class GlobalSearchForm(forms.Form):
    q = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Cari konten...',
            'hx-get': '/cms/search/',
            'hx-trigger': 'input changed delay:300ms',
            'hx-target': '#search-results',
        })
    )
    content_type = forms.ChoiceField(
        required=False,
        choices=[('', 'Semua')] + ContentCategory.CONTENT_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
