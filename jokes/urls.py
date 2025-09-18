from django.urls import path
from . import views

urlpatterns = [
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_joke/<int:category_id>/', views.add_joke, name='add_joke'),
    path('edit_joke/<int:joke_id>/', views.edit_joke, name='edit_joke'),
    path('add_topper/<int:joke_id>/', views.add_topper, name='add_topper'),
]