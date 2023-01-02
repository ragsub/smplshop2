from django.db.models import F, FilteredRelation, Q, Value
from django.contrib.auth import get_user_model
from smplshop.users.tenant.models import Shop
from .master.models import Product
from .transaction.models import Cart, CartItem
from .transaction.logic import CartLogic
from .models import Address

User = get_user_model()


class ShopFrontLogic:
    def __init__(self, shop: Shop):
        self.shop = shop

    def get_shop_products_with_cart_items(self, request):

        qs = Product.objects.all()

        if CartLogic.is_cart_available(request=request):
            cart = CartLogic(request).get_cart()

            qs = (
                qs.prefetch_related("cart_items")
                .prefetch_related("cartitem")
                .values("uuid", "shop", "name", "price")
                .annotate(
                    item_in_cart=FilteredRelation(
                        "cartitem", condition=Q(cartitem__cart=cart)
                    )
                )
                .annotate(quantity=F("item_in_cart__quantity"))
            )
        else:
            qs = qs.annotate(quantity=Value(0))

        return qs
