import uuid
from django.contrib.auth import get_user_model

from smplshop.users.tenant.models import Shop
from smplshop.shop.models import Address

from .models import ShopDetails, UserAddress, Product

User = get_user_model()


class AddressForShopLogic:
    def __init__(self, shop: Shop):
        self.shop = shop

    def add_or_update_address(self, address: Address):
        if self.is_present():
            shop_detail = ShopDetails.objects.get(shop=self.shop)
            shop_detail.address = address
            shop_detail.save()
        else:
            ShopDetails.objects.create(address=address)

    def is_present(self):
        return True if ShopDetails.objects.filter(shop=self.shop).exists() else False

    def get(self):
        return ShopDetails.objects.get(shop=self.shop) if self.is_present() else None


class AddressForUserLogic:
    def __init__(self, user: User):  # type:ignore
        self.user = user

    def get_all_address_for_user(self):
        return UserAddress.objects.filter(user=self.user)

    def add_address_to_user(self, address: Address):
        UserAddress.objects.create(user=self.user, address=address)


class ProductLogic:
    def __init__(self, product: Product):
        self.product = product

    def get_product(self):
        return self.product

    @staticmethod
    def is_valid_product(shop: Shop, product_uuid: str):
        return (
            True
            if Product.objects.filter(shop=shop, uuid=product_uuid).exists()
            else False
        )

    @staticmethod
    def get_product_from_uuid(shop: Shop, product_uuid: str):
        if ProductLogic.is_valid_product(shop, product_uuid):
            return Product.objects.get(shop=shop, uuid=product_uuid)
        else:
            return None
