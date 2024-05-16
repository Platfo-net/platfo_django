from django.urls import path

from account.views.auth_view import LoginPhoneNumberView, ForgotPasswordView
from account.views.user_view import RegisterByPhoneNumberView, UpdateUserView, \
    ChangeUserPasswordView, GetUserMeView, UploadUserProfileImageView

urlpatterns = [
    # user
    path('phone-register/', RegisterByPhoneNumberView.as_view(), name='phone-register'),
    path('update-user/', UpdateUserView.as_view(), name='update-user'),
    path('change-password-user/', ChangeUserPasswordView.as_view(), name='change-password-user'),
    path('get-user-me/', GetUserMeView.as_view(), name='get-user-me'),
    path('upload-user-profile/', UploadUserProfileImageView.as_view(), name='upload-user-profile'),
    # auth
    path('login-phone-number/', LoginPhoneNumberView.as_view(), name='login-phone-number'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
]
