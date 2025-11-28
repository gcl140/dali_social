from django.urls import path
from . import views

urlpatterns = [
    path('', views.connection_list, name='connection_list'),
    path('request/<int:pk>/', views.send_connection_request, name='send_connection_request'),
    path('accept/<int:pk>/', views.accept_connection_request, name='accept_connection_request'),
    path('reject/<int:pk>/', views.reject_connection_request, name='reject_connection_request'),
]