import uuid

from smplshop.users.tenant.models import Shop
from smplshop.shop.master.models import Product
from smplshop.shop.models import Address
from .models import Cart, CartItem
from .exceptions import ShopNotFoundException, CartNotFoundException


class CartLogic:
    def __init__(self, request):
        if request.shop is None:
            raise ShopNotFoundException("CartLogic: Shop cannot be empty")
        else:
            self.shop = request.shop

        if not CartLogic.is_cart_available(request):
            self.cart = Cart.objects.create(shop=self.shop)
            request.session[self.shop.code] = str(self.cart.uuid)
        else:
            cart_uuid = request.session.get(self.shop.code, "None")
            self.cart = Cart.objects.get(shop=self.shop, uuid=cart_uuid)

    @staticmethod
    def is_cart_available(request):
        cart_uuid = request.session.get(request.shop.code, None)
        if cart_uuid is None:
            cart_available = False
        elif Cart.objects.filter(shop=request.shop, uuid=str(cart_uuid)).exists():
            cart_available = True
        else:
            raise CartNotFoundException(
                "CartLogic: Cart matching cart id and shop not found"
            )

        return cart_available

    def get_cart(self):
        return self.cart

    def get_cart_and_items(self):
        return CartItem.objects.filter(cart=self.cart)

    def add_to_cart(self, product: Product):
        cart_item, created = CartItem.objects.get_or_create(
            cart=self.cart, product=product
        )
        cart_item.quantity = cart_item.quantity + 1
        cart_item.save()

class OrderLogic:
    def __init__(self, cart:Cart, address:Address):
        