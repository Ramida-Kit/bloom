from django.urls import path
from . import views

app_name = 'joke_sets'

urlpatterns = [
    path('set/<int:set_id>/', views.joke_set_detail, name='joke_set_detail'),
    path('add_joke_to_set/<int:set_id>/', views.add_joke_to_set, name='add_joke_to_set'),
]