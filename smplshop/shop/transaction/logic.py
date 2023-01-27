from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from smplshop.shop.master.models import Product
from smplshop.shop.models import Address
from .models import Cart, CartItem, Order, OrderItem
from .exceptions import (
    ShopNotFoundException,
    CartNotFoundException,
    OrderNotFoundException,
    IncorrectInputsException,
)

User = get_user_model()


class CartLogic:
    def __init__(self, request: HttpRequest):
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

        self.request = request

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

    def get_shop(self):
        return self.shop

    def get_cart_and_items(self):
        return CartItem.objects.filter(cart=self.cart)

    def add_to_cart(self, product: Product):
        cart_item, created = CartItem.objects.get_or_create(
            cart=self.cart, product=product
        )
        cart_item.quantity = cart_item.quantity + 1
        cart_item.save()

    def delete_cart(self):
        self.cart.delete()
        del self.request.session[self.shop.code]
        self.request.session.modified = True


class OrderLogic:
    def __init__(
        self,
        request: HttpRequest = None,  # type:ignore
        address: Address = None,  # type:ignore
        order_uuid=None,  # type:ignore
    ):

        if order_uuid is None:
            if request is None or address is None:
                raise IncorrectInputsException(
                    "OrderLogic: Request and address cannot be empty"
                )
            cart_logic = CartLogic(request=request)
            if cart_logic.get_cart_and_items():
                self.order = Order.objects.create(
                    shop=cart_logic.get_shop(), user=request.user, address=address
                )
                for item in cart_logic.get_cart_and_items():
                    OrderItem.objects.create(
                        order=self.order,
                        product=item.product,
                        price=item.product.price,
                        quantity=item.quantity,
                    )
                cart_logic.delete_cart()
        else:
            if Order.objects.filter(uuid=order_uuid).exists():
                self.order = Order.objects.get(uuid=order_uuid)
            else:
                raise OrderNotFoundException(
                    "OrderLogic: Order with uuid does not exists"
                )

    def get_order(self):
        return self.order

    @staticmethod
    def get_order_by_user(user: User):
        return Order.objects.filter(user=user)

    def change_status(self, status_change: str):
        if status_change == "accept":
            self.order.accept_order()

        elif status_change == "ship":
            self.order.ship_order()

        elif status_change == "deliver":
            self.order.deliver_order()

        elif status_change == "close":
            self.order.close_order()

        elif status_change == "cancel":
            self.order.cancel_order()
        else:
            raise ValidationError(
                _("{}{}{}".format("Order status ", status_change, " is incorrect"))
            )
