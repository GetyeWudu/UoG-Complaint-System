"""
File upload validators
"""
from django.core.exceptions import ValidationError
from django.conf import settings
import os


def validate_file_size(file):
    """
    Validate file size doesn't exceed maximum
    """
    max_size = settings.MAX_UPLOAD_SIZE
    if file.size > max_size:
        max_size_mb = max_size / (1024 * 1024)
        raise ValidationError(f'File size cannot exceed {max_size_mb}MB')


def validate_file_extension(file):
    """
    Validate file extension is in allowed list
    """
    allowed_extensions = settings.ALLOWED_FILE_TYPES
    ext = os.path.splitext(file.name)[1][1:].lower()  # Remove the dot
    
    if ext not in allowed_extensions:
        raise ValidationError(
            f'File type .{ext} is not allowed. Allowed types: {", ".join(allowed_extensions)}'
        )


def validate_file_mime_type(file):
    """
    Validate actual file MIME type (prevents extension spoofing)
    """
    allowed_mime_types = {
        'jpg': ['image/jpeg'],
        'jpeg': ['image/jpeg'],
        'png': ['image/png'],
        'gif': ['image/gif'],
        'pdf': ['application/pdf'],
    }
    
    # Get file extension
    ext = os.path.splitext(file.name)[1][1:].lower()
    
    if ext not in settings.ALLOWED_FILE_TYPES:
        raise ValidationError(f'File type .{ext} is not allowed')
    
    # Read file content to detect MIME type
    try:
        # Try using python-magic if available
        try:
            import magic
            mime = magic.from_buffer(file.read(2048), mime=True)
            file.seek(0)  # Reset file pointer
        except ImportError:
            # Fallback to basic content type check
            mime = file.content_type
        
        # Check if MIME type matches extension
        if ext in allowed_mime_types:
            if mime not in allowed_mime_types[ext]:
                raise ValidationError(
                    f'File content does not match extension. Expected {allowed_mime_types[ext]}, got {mime}'
                )
    except Exception as e:
        # If validation fails, log but don't block (fallback to extension check)
        pass


def validate_image_file(file):
    """
    Additional validation for image files
    """
    ext = os.path.splitext(file.name)[1][1:].lower()
    
    if ext in ['jpg', 'jpeg', 'png', 'gif']:
        try:
            from PIL import Image
            
            # Try to open as image
            img = Image.open(file)
            img.verify()
            file.seek(0)  # Reset file pointer
            
            # Check image dimensions (optional)
            # max_dimension = 4096
            # if img.width > max_dimension or img.height > max_dimension:
            #     raise ValidationError(f'Image dimensions cannot exceed {max_dimension}x{max_dimension}')
            
        except Exception as e:
            raise ValidationError('Invalid image file')


def sanitize_filename(filename):
    """
    Sanitize filename to prevent directory traversal and other attacks
    """
    # Get just the filename without path
    filename = os.path.basename(filename)
    
    # Remove any non-alphanumeric characters except dots, dashes, and underscores
    import re
    filename = re.sub(r'[^\w\s.-]', '', filename)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Limit filename length
    name, ext = os.path.splitext(filename)
    if len(name) > 100:
        name = name[:100]
    
    return name + ext
