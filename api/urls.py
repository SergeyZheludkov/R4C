from django.urls import path

from .views import RobotCreateView

urlpatterns = [
    path('robot_production/', RobotCreateView.as_view()),
]
