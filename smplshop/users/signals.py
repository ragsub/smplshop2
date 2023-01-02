from django.dispatch import receiver
from django.http.request import HttpRequest
from django.http import Http404
from django.utils.translation import gettext_lazy as _

from allauth.account.signals import user_logged_in


from .models import User
from .logic import ShopForUserLogic


@receiver(user_logged_in)
def add_tenant_to_user(sender, request: HttpRequest, user: User, *args, **kwargs):
    shop_for_user = ShopForUserLogic(user)

    if not shop_for_user.has_current_shop():
        shop = shop_for_user.get_shop()
        if shop is not None:
            shop_for_user.set_current_shop(shop)
        else:
            raise Http404("{}{}".format(_("No shop is mapped to User:"), user))
