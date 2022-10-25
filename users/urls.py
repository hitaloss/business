from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views

urlpatterns = [
    path("login/", obtain_auth_token),
    path("accounts/", views.UserView.as_view()),
    path("accounts/newest/<int:num>/", views.UserView.as_view()),
    path("accounts/<pk>/", views.UserUpdateView.as_view()),
    path("accounts/<pk>/management/", views.UserManagementView.as_view()),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
