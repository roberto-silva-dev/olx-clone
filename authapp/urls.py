from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='authapp/login.html',
        redirect_authenticated_user=True,
        next_page='home'
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.registrar, name='register'),
] 