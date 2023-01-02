from django.contrib.auth import get_user_model
from smplshop.users.logic import ShopForUserLogic
from .models import Shop

User = get_user_model()


class TenantContextLogic:
    def __init__(self, user: User, path: str):  # type:ignore
        self.user = user
        self.path = path

    def is_required(self):
        shop = None
        tenant_context = None

        if self.is_admin_site():
            tenant_context = False

        elif self.is_shop_site():
            tenant_context = True
            self.shop = self.get_shop_object(self.get_shop_name())

        elif self.is_user_authenticated():
            tenant_context = True
            user_to_shop = ShopForUserLogic(self.user)
            self.shop = user_to_shop.get_shop()

        else:
            tenant_context = False

        return tenant_context

    def get_shop(self):
        if self.is_required():
            return self.shop
        else:
            return None

    def is_admin_site(self):
        site = self.extract_site(self.path)
        return True if site == "admin" else False

    def is_shop_site(self):
        site = self.extract_site(self.path)
        return True if site == "shop" else False

    def is_user_authenticated(self):
        return self.user.is_authenticated

    def extract_site(self, path: str):
        path_strings = path.split("/")
        return path_strings[1]

    def get_shop_name(self):
        path_strings = self.path.split("/")
        return path_strings[2]

    def get_shop_object(self, shop_name: str):
        if Shop.objects.filter(code=shop_name).exists():
            return Shop.objects.get(code=shop_name)
        else:
            return None


class TenantLogic:
    def __init__(self, code: str):
        self.code = code

    def is_validated(self):
        return False if Shop.objects.filter(code=self.code).exists() else True

    def create(self, name: str):
        new_shop = Shop.objects.create(code=self.code, name=name)
        new_shop.save()
        return new_shop
