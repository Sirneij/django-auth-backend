from django.urls import path

from users.views import confirm, login, logout, regenerate, register

app_name = 'users'
urlpatterns = [
    path('register/', register.RegisterView.as_view(), name='register'),
    path('register/confirm/<uidb64>/<token>/', confirm.ConfirmEmailView.as_view(), name='confirm'),
    path('regenerate-token/', regenerate.RegenerateTokenView.as_view(), name='regenerate'),
    path('login/', login.LoginPageView.as_view(), name='login'),
    path('logout/', logout.LogoutView.as_view(), name='logout'),
]
