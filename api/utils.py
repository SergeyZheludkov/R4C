from django.http import JsonResponse


class UTF8JsonResponse(JsonResponse):
    """Отключение замены кириллицы в 'uXXXX' при конвертации в JSON."""

    def __init__(self, *args, json_dumps_params=None, **kwargs):
        json_dumps_params = {
            "ensure_ascii": False, **(json_dumps_params or {})
        }
        super().__init__(*args, json_dumps_params=json_dumps_params, **kwargs)
