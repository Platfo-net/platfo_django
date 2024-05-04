from django.urls import path

from account.views import RegisterByPhoneNumberView

urlpatterns = [
    path('phone-register/', RegisterByPhoneNumberView.as_view(), name='phone-register'),
]
