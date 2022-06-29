from django.urls import path

from . import views

urlpatterns = [
    path('', views.rooms, name='bots'),
    path('<slug:slug>/', views.room, name='bot'),
    path('<slug:slug>/edit/', views.room_edit, name='edit'),
]
