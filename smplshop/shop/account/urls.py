from django.urls import path, re_path
from allauth.account.views import (
    SignupView,
    LoginView,
    ConfirmEmailView,
    EmailView,
    PasswordChangeView,
    PasswordSetView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetFromKeyView,
    PasswordResetFromKeyDoneView,
    LogoutView,
    AccountInactiveView,
    EmailVerificationSentView,
)


app_name = "smplshop.shop.account"
urlpatterns = [
    path(
        "signup/",
        SignupView.as_view(template_name="shop/account/signup.html"),
        name="buyer_account_signup",
    ),
    path(
        "login/",
        LoginView.as_view(template_name="shop/account/login.html"),
        name="buyer_account_login",
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="shop/account/logout.html"),
        name="buyer_account_logout",
    ),
    path(
        "password/change/",
        PasswordChangeView.as_view(template_name="shop/account/password_change.html"),
        name="buyer_account_change_password",
    ),
    path(
        "password/set/",
        PasswordSetView.as_view(template_name="shop/account/password_set.html"),
        name="buyer_account_set_password",
    ),
    path(
        "inactive/",
        AccountInactiveView.as_view(template_name="shop/account/account_inactive.html"),
        name="buyer_account_inactive",
    ),
    # E-mail
    path(
        "email/",
        EmailView.as_view(template_name="shop/account/email.html"),
        name="buyer_account_email",
    ),
    path(
        "confirm-email/",
        EmailVerificationSentView.as_view(
            template_name="shop/account/verification_sent.html"
        ),
        name="buyer_account_email_verification_sent",
    ),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(template_name="shop/account/email_confirm.html"),
        name="buyer_account_confirm_email",
    ),
    # password reset
    path(
        "password/reset/",
        PasswordResetView.as_view(template_name="shop/account/password_reset.html"),
        name="buyer_account_reset_password",
    ),
    path(
        "password/reset/done/",
        PasswordResetDoneView.as_view(
            template_name="shop/account/password_reset_done.html"
        ),
        name="buyer_account_reset_password_done",
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        PasswordResetFromKeyView.as_view(
            template_name="shop/account/password_reset_from_key.html"
        ),
        name="buyer_account_reset_password_from_key",
    ),
    path(
        "password/reset/key/done/",
        PasswordResetFromKeyDoneView.as_view(
            template_name="password_reset_from_key_done.html"
        ),
        name="buyer_account_reset_password_from_key_done",
    ),
]