from django.urls import path
from . import views

urlpatterns = [
    path('past-results/', views.past_results, name='past_results'),
]
