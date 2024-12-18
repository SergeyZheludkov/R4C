from django.urls import path

from .views import robots_excel_table

urlpatterns = [
    path('', robots_excel_table, name='robots_excel_table'),
]
