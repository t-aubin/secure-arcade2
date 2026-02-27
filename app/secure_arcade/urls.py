"""
URL configuration for secure_arcade project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views as core_views
from tictactoe import views as ttt_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', core_views.home, name="home"),
    path('dashboard/', core_views.dashboard, name="dashboard"),
    path('register/', core_views.register, name="register"),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('game/new/', ttt_views.new_game, name='new_game'),
    path('game/<int:game_id>/', ttt_views.game_detail, name='game_detail'),
    path('game/<int:game_id>/move/<int:position>/', ttt_views.make_move, name='make_move'),
]