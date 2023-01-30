from django.urls import path

from users.views import APIGetToken, APISignup

urlpatterns = [
    path('token/', APIGetToken.as_view(), name='get_token'),
    path('signup/', APISignup.as_view(), name='signup'),
]
