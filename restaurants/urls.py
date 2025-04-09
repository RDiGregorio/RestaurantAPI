from django.urls import path
from . import views

urlpatterns = [
    path('open-restaurants/', views.open_restaurants, name='open-restaurants'),
]