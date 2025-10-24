from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),  # Root URL
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_joke/<int:category_id>/', views.add_joke, name='add_joke'),
    path('edit_joke/<int:joke_id>/', views.edit_joke, name='edit_joke'),
    path('add_topper/<int:joke_id>/', views.add_topper, name='add_topper'),
    path('joke-sets/', views.joke_sets, name='joke_sets'),
    path('joke-sets/<int:joke_set_id>/', views.joke_set_detail, name='joke_set_detail'),
]