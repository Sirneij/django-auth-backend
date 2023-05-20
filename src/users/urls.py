from django.urls import path

from users.views import (
    confirm,
    current_user,
    login,
    logout,
    profile_update,
    regenerate,
    register,
    series,
)
from users.views.password import change_password, confirm_change_request, request_change

app_name = 'users'
urlpatterns = [
    path('register/', register.RegisterView.as_view(), name='register'),
    path(
        'register/confirm/<uidb64>/<token>/',
        confirm.ConfirmEmailView.as_view(),
        name='confirm',
    ),
    path(
        'regenerate-token/', regenerate.RegenerateTokenView.as_view(), name='regenerate'
    ),
    path('login/', login.LoginPageView.as_view(), name='login'),
    path('logout/', logout.LogoutView.as_view(), name='logout'),
    # Password change
    path(
        'password-change/request-password-change/',
        request_change.RequestPasswordChangeView.as_view(),
        name='request_password_change',
    ),
    path(
        'password-change/confirm/change-password/<uidb64>/<token>/',
        confirm_change_request.ConfirmPasswordChangeRequestView.as_view(),
        name='confirm_password_change_request',
    ),
    path(
        'password-change/change-user-password/',
        change_password.ChangePasswordView.as_view(),
        name='change_password',
    ),
    # User
    path('current-user/', current_user.CurrentUserView.as_view(), name='current_user'),
    path(
        'update-user/', profile_update.UserUpdateView.as_view(), name='profile_update'
    ),
    # Series
    path('series/', series.SeriesDataView.as_view(), name='series_data'),
]
