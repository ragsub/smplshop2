from django.urls import path
from allauth.account.views import SignupView

from .views import (
    ShopFrontView,
    AddToCart,
    CartView,
    OrderListView,
    SelectAddressView,
    AddAddressForUserView,
)

app_name = "smplshop.shop"
urlpatterns = [
    path("<str:shop>/signup/", view=SignupView.as_view(), name="signup_buyer"),
    path("<str:shop>/", view=ShopFrontView.as_view(), name="shop_front"),
    path(
        "<str:shop>/cart/add/<uuid:product_uuid>/",
        view=AddToCart.as_view(),
        name="add_to_cart",
    ),
    path("<str:shop>/cart/", view=CartView.as_view(), name="cart"),
    path(
        "<str:shop>/cart/address",
        view=SelectAddressView.as_view(),
        name="select_address",
    ),
    path(
        "<str:shop>/cart/address/add",
        view=AddAddressForUserView.as_view(),
        name="add_address",
    ),
    path("<str:shop>/orders/", view=OrderListView.as_view(), name="customer_orders"),
]
