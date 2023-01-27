from django.contrib.auth import get_user_model
from .tenant.models import Shop

from .models import CurrentShopForUser, UserToShop

User = get_user_model()


class ShopForUserLogic:
    def __init__(self, user: User):
        self.user = user

    def get_shop(self):
        if self.has_current_shop():
            current_shop = CurrentShopForUser.objects.get(user=self.user).shop
            if not UserToShop.objects.filter(
                user=self.user, shop=current_shop
            ).exists():
                current_shop = None
        else:
            current_shop = (
                UserToShop.objects.filter(user=self.user).first().shop
                if UserToShop.objects.filter(user=self.user).exists()
                else None
            )
        return current_shop

    def add_owned_shop(self, shop: Shop):
        self.user.shop.add(shop, through_defaults={"role": "owner"})
        return

    def add_buyer_shop(self, shop: Shop):
        self.user.shop.add(shop, through_defaults={"role": "buyer"})
        return

    def has_current_shop(self):
        return (
            True
            if CurrentShopForUser.objects.filter(user=self.user).exists()
            else False
        )

    def set_current_shop(self, shop: Shop):
        CurrentShopForUser.objects.create(user=self.user, shop=shop)
        return
