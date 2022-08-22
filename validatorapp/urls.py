from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('return-csv/', views.return_csv),
]