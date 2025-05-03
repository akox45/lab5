from django.urls import path
from . import views

urlpatterns = [
    path('', views.photo_list, name='photo_list'),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('photo/upload/', views.photo_upload, name='photo_upload'),
    path('photo/<int:photo_id>/delete/', views.photo_delete, name='photo_delete'),
]