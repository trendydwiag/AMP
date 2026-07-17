from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        label='Nama',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan nama Anda',
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan email Anda',
        })
    )
    subject = forms.CharField(
        max_length=300,
        label='Subjek',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan subjek pesan',
        })
    )
    message = forms.CharField(
        label='Pesan',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Tulis pesan Anda di sini...',
            'rows': 6,
        })
    )


class NewsletterForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan email Anda untuk berlangganan',
        })
    )
