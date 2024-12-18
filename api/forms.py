from django import forms

from robots.models import Robot


class RobotForm(forms.ModelForm):
    """Форма на основе модели  Robots.

    Используется для валидации введенных в api-запросе данных
    на соответствие параметрам модели.
    """

    class Meta:
        model = Robot
        fields = ('model', 'version', 'created')
