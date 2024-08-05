from django.urls import path
from . import views

urlpatterns = [
    path('register-rider/', views.register_rider, name = 'register-rider'),
    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_user, name = 'logout'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
]