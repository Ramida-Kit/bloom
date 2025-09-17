from django.urls import path
from . import views

urlpatterns = [
    path('set/<int:set_id>/', views.joke_set_detail, name='joke_set_detail'),
]