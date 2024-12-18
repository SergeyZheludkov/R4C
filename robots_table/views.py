from datetime import datetime as dt, timedelta

from django.http import HttpResponse
from openpyxl import Workbook

from robots.models import Robot

HEADERS = ['Модель', 'Версия', 'Количество за неделю']


def robots_excel_table(request):
    """Выгрузка Excel-файл со сводкой по роботам.

    Сводка по суммарным показателям производства роботов за последнюю неделю,
    с разбивкой по моделям постранично.
    """
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="robots.xlsx"'
    workbook = Workbook()

    robots = Robot.objects.all()
    model_version = set([(robot.model, robot.version) for robot in robots])

    now = dt.now()
    created_since = now - timedelta(days=7)
    sheet_list = []

    for model, version in model_version:
        if model not in sheet_list:
            sheet_list.append(model)
            worksheet = workbook.create_sheet(model)
            worksheet.append(HEADERS)
        else:
            worksheet = workbook[model]

        robots_count = robots.filter(model=model, version=version,
                                     created__gte=created_since).count()
        worksheet.append([model, version, robots_count])

    del workbook['Sheet']
    workbook.save(response)

    return response
