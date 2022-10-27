from django.conf.urls import url
from rest_framework.authtoken import views
from .views import CreateUserAPIView, LogoutUserAPIView


urlpatterns = [
    url(r'^auth/login/$',
        views.obtain_auth_token,
        name='auth_user_login'),
    url(r'^auth/register/$',
        CreateUserAPIView.as_view(),
        name='auth_user_create'),
    url(r'^auth/logout/$',
        LogoutUserAPIView.as_view(),
        name='auth_user_logout')
]
