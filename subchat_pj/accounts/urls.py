from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name="signup"),
    path('emoji/', views.emoji, name="emoji"),
    path('emoji_modify/<str:new_emoji>', views.emoji_modify, name="emoji_modify"),
]