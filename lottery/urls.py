from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_lottery_table, name='show_lottery_table'),
]
