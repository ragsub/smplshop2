from django.urls import path

from .views import SignupUserAndTenant

app_name = "smplshop.users.tenant"
urlpatterns = [
    path("signup/", view=SignupUserAndTenant.as_view(), name="user_and_tenant_signup"),
]
