from django import forms
from .models import Article, Category, Tag


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title', 'slug', 'excerpt', 'content', 'featured_image',
            'category', 'author_name', 'status', 'priority', 'featured',
            'allow_comments', 'content_format', 'seo_title', 'seo_description',
            'og_title', 'og_description', 'og_image', 'twitter_card',
            'canonical_url', 'robots', 'scheduled_at', 'publish_end_date',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 20}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'author_name': forms.TextInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'content_format': forms.Select(attrs={'class': 'form-select'}),
            'seo_title': forms.TextInput(attrs={'class': 'form-input'}),
            'seo_description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'og_title': forms.TextInput(attrs={'class': 'form-input'}),
            'og_description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'twitter_card': forms.Select(attrs={'class': 'form-select'}),
            'canonical_url': forms.URLInput(attrs={'class': 'form-input'}),
            'robots': forms.Select(attrs={'class': 'form-select'}),
            'scheduled_at': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'publish_end_date': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Judul artikel wajib diisi.")
        if len(title) < 5:
            raise forms.ValidationError("Judul artikel minimal 5 karakter.")
        return title

    def save(self, commit=True):
        article = super().save(commit=False)
        if not article.slug:
            from django.utils.text import slugify
            article.slug = slugify(article.title)
        if commit:
            article.save()
        return article


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
        }
