import json
from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .forms import RobotForm
from .utils import UTF8JsonResponse
from .validators import validate_existing_model


@method_decorator(csrf_exempt, name='dispatch')
class RobotCreateView(View):
    """Добавление в БД записи о новом роботе."""

    def post(self, request):
        raw_robot_data = json.loads(request.body)
        form = RobotForm(raw_robot_data)

        if not form.is_valid():
            return UTF8JsonResponse(
                data={'message': form.errors}, status=HTTPStatus.BAD_REQUEST
            )

        model = form.cleaned_data.get('model')
        version = form.cleaned_data.get('version')

        try:
            validate_existing_model(model)
        except ValidationError as error:
            return UTF8JsonResponse(
                data={'message': f'Ошибка в исходных данных: {error.message}'},
                status=HTTPStatus.BAD_REQUEST
            )

        form.instance.serial = f'{model}-{version}'
        form.save()

        data = {
            'message': f'Новый робот был добавлен в базу данных'
            f' с серийным номером {form.instance.serial}'
        }
        return UTF8JsonResponse(data, status=HTTPStatus.CREATED)
