from django.urls import path
from .views import (
    CreeateShopDetails,
    UpdateShopDetails,
    ChooseAddorUpdateShopDetails,
    ProductList,
    AddProduct,
)

app_name = "smplshop.shop.master"

urlpatterns = [
    path(
        "details/~redirect/",
        view=ChooseAddorUpdateShopDetails.as_view(),
        name="choose_add_or_update_shop_details",
    ),
    path("details/add/", view=CreeateShopDetails.as_view(), name="add_shop_details"),
    path(
        "details/update/<uuid:uuid>/",
        view=UpdateShopDetails.as_view(),
        name="update_shop_details",
    ),
    path(
        "products/",
        view=ProductList.as_view(),
        name="view_products",
    ),
    path(
        "products/add",
        view=AddProduct.as_view(),
        name="add_product",
    ),
]
