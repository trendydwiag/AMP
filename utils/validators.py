from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
import os
import mimetypes

def validate_file_upload(
    file: UploadedFile, 
    max_size_mb: float = 5.0, 
    allowed_extensions: list[str] = None
) -> None:
    """Validates file upload sizes and extensions to prevent denial of service and remote execution.

    Args:
        file: The uploaded file object.
        max_size_mb: Maximum size permitted in Megabytes.
        allowed_extensions: List of allowed file extensions (e.g., ['.jpg', '.png', '.pdf']).
    """
    # 1. Size Validation
    max_size_bytes = max_size_mb * 1024 * 1024
    if file.size > max_size_bytes:
        raise ValidationError(
            f"Ukuran file ({file.size / (1024 * 1024):.2f} MB) melebihi batas maksimal {max_size_mb} MB."
        )

    # 2. Extension and Mime-type Validation
    ext = os.path.splitext(file.name)[1].lower()
    
    # Default allowed extensions if none provided (secure defaults: images, documents, PDFs)
    if allowed_extensions is None:
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.csv', '.txt']

    if ext not in allowed_extensions:
        raise ValidationError(
            f"Format file '{ext}' tidak diizinkan. Ekstensi yang diperbolehkan: {', '.join(allowed_extensions)}."
        )

    # Check mime type to prevent malicious extension spoofing (e.g., renaming a .sh script to .png)
    mime_type, _ = mimetypes.guess_type(file.name)
    if mime_type:
        dangerous_mimes = [
            'application/x-sh', 'application/x-msdownload', 'application/x-executable',
            'text/html', 'text/javascript', 'application/javascript'
        ]
        if mime_type in dangerous_mimes:
            raise ValidationError("Tipe konten file terdeteksi berbahaya dan diblokir.")
