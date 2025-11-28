from django.urls import path
from . import views

urlpatterns = [
    path('', views.member_list, name='member_list'),
    path('search/', views.search_members, name='search_members'),
    path('<int:pk>/', views.member_detail, name='member_detail'),


    # path('profile/', views.profile_view, name='profile_member'),
    # path('profile/edit/', views.profile_update, name='profile_update'),
    path("edit/", views.profile_update, name="member_edit_create"),
    path("edit/<int:member_id>/", views.profile_update, name="member_edit"),
    path('<int:member_id>/', views.profile_view, name='member_profile'),
    path('my_profile/', views.profile_view, name='my_profile'),
]

# API URLs - include them in the main urls.py instead