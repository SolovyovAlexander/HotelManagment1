from django.urls import path, include
from rest_framework import routers

from account.views import registration_view, Logout, ChangePasswordView, AccountViewSet
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account'

router = routers.DefaultRouter()

router.register(r'accounts', AccountViewSet, basename='accounts')

urlpatterns = [
    path('register', registration_view),
    path('login', obtain_auth_token),
    path('logout', Logout.as_view()),
    path('change_password', ChangePasswordView.as_view()),
    path('', include(router.urls))
]
