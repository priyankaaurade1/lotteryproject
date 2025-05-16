from django.urls import path
from . import views
from .cron import run_cron_job

urlpatterns = [
    path('past-results/', views.past_results, name='past_results'),
    path('run-generator/', run_cron_job, name='run_generator'),
]
