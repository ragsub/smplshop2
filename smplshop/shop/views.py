import uuid
from django.views.generic import ListView, View, CreateView
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .master.models import Product, Address
from .master.logic import AddressForUserLogic, ProductLogic
from .transaction.logic import CartLogic, OrderLogic
from .logic import ShopFrontLogic
from .exceptions import ProductNotFoundException
from .forms import SelectAddressForm


class ShopFrontView(View):
    template_name = "shop/shop_front.html"

    def get(self, request, *args, **kwargs):
        shop_front = ShopFrontLogic(request.shop)
        context = {}
        context["object_list"] = shop_front.get_shop_products_with_cart_items(
            request  # type:ignore
        )

        return render(
            request=request, template_name=self.template_name, context=context
        )


class AddToCart(View):
    def setup(self, request, *args, **kwargs):
        self.cart = CartLogic(request)
        product_uuid = kwargs.get("product_uuid", None)
        if not ProductLogic.is_valid_product(
            shop=request.shop, product_uuid=str(product_uuid)
        ):
            raise ProductNotFoundException("Product UUID cannot be blanks")
        else:
            self.product_logic = ProductLogic(
                ProductLogic.get_product_from_uuid(request.shop, product_uuid)
            )

        self.product = self.product_logic.get_product()
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.cart.add_to_cart(product=self.product)

        return redirect(reverse("smplshop.shop:shop_front", args=[request.shop.code]))


class CartView(View):
    def setup(self, request, *args, **kwargs):
        self.shop = request.shop  # type:ignore
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        if CartLogic.is_cart_available(request):
            cart = CartLogic(request)
            context["object_list"] = cart.get_cart_and_items()
            context["total_cart_price"] = cart.get_cart().total_cart_price

        return render(request=request, template_name="shop/cart.html", context=context)


class OrderListView(LoginRequiredMixin, ListView):
    pass


class SelectAddressView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.user = request.user
        self.cart = CartLogic(request)
        self.address_for_user = AddressForUserLogic(request.user)

        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        context["form"] = SelectAddressForm(
            addresses=self.address_for_user.get_all_address_for_user()
        )
        return render(
            request=request, template_name="shop/select_address.html", context=context
        )

    def post(self, request, *args, **kwargs):
        form = SelectAddressForm(
            request.POST, addresses=self.address_for_user.get_all_address_for_user()
        )
        if form.is_valid():
            order_address = form.cleaned_data["address"]
            if CartLogic.is_cart_available(request=request):
                cart_logic = CartLogic(request)

            order = OrderLogic(cart=CartLogic.get_cart(), address=order_address)


class AddAddressForUserView(LoginRequiredMixin, CreateView):
    model = Address
    template_name = "shop/add_user_address.html"
    fields = ["name", "address1", "address2", "city", "zip_code", "country", "phone"]

    def form_valid(self, form):
        success_url = super().form_valid(form)
        address_for_user = AddressForUserLogic(self.request.user)  # type:ignore
        address_for_user.add_address_to_user(self.object)  # type:ignore
        return success_url

    def get_success_url(self):
        return reverse(
            "smplshop.shop:select_address",
            kwargs={"shop": self.request.shop.code},  # type:ignore
        )
