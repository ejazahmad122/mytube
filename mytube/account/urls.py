from django.urls import path, include
from .views import SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegistrationView, UserResetPasswordView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('sent-password-reset-email/', SendPasswordResetEmailView.as_view(), name='resetpasswordemail'),
    path('reset-password/<uid>/<token>/', UserResetPasswordView.as_view(), name='setnewpassword')
]
