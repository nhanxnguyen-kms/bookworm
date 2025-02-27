from django.core.exceptions import ValidationError


def validate_cover_image(image) -> None:
    max_size = 2 * 1024 * 1024  # 2MB
    valid_extensions = ["jpg", "jpeg", "png"]
    if image.size > max_size:
        raise ValidationError(
            f"Image size should not exceed {max_size / (1024 * 1024)} MB."
        )
    if not any(image.name.lower().endswith(ext) for ext in valid_extensions):
        raise ValidationError(
            f"Image must be one of the following formats: {', '.join(valid_extensions)}."
        )
