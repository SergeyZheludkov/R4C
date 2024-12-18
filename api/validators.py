from django.core.exceptions import ValidationError

from robots.models import Robot


def validate_existing_model(value):
    """Проверка наличия модели робота в БД."""
    if not Robot.objects.filter(model=value).exists():
        raise ValidationError('данной модели нет в базе данных')
