from django.urls import reverse
from django.views.generic import CreateView, UpdateView, RedirectView, ListView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from smplshop.shop.models import Address
from .models import Product
from .logic import AddressForShopLogic


class ChooseAddorUpdateShopDetails(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        address_for_shop = AddressForShopLogic(self.request.shop)  # type:ignore
        if address_for_shop.is_present():
            return reverse(
                "smplshop.shop.master:update_shop_details",
                args=[str(address_for_shop.get().address.uuid)],  # type:ignore,
            )
        else:
            return reverse("smplshop.shop.master:add_shop_details")


class ShopDetailsNotAvailableTest(UserPassesTestMixin):
    def test_func(self):
        address_for_shop = AddressForShopLogic(self.request.shop)  # type:ignore
        return False if address_for_shop.is_present() else True


class ShopDetailsAvailableTest(UserPassesTestMixin):
    def test_func(self):
        address_for_shop = AddressForShopLogic(self.request.shop)  # type:ignore
        return True if address_for_shop.is_present() else False


class CreeateShopDetails(LoginRequiredMixin, ShopDetailsNotAvailableTest, CreateView):
    model = Address
    template_name = "shop/master/add_shop_details.html"
    fields = ["name", "address1", "address2", "city", "zip_code", "country", "phone"]

    def form_valid(self, form):
        success_url = super().form_valid(form)
        address_for_shop = AddressForShopLogic(self.request.shop)  # type:ignore
        address_for_shop.add_or_update_address(self.object)  # type:ignore
        return success_url

    def get_success_url(self):
        return reverse("smplshop.shop.master:choose_add_or_update_shop_details")


class UpdateShopDetails(LoginRequiredMixin, ShopDetailsAvailableTest, UpdateView):
    model = Address
    template_name = "shop/master/update_shop_details.html"
    fields = ["name", "address1", "address2", "city", "zip_code", "country", "phone"]
    slug_url_kwarg = "uuid"
    slug_field = "uuid"

    def form_valid(self, form):
        success_url = super().form_valid(form)
        address_for_shop = AddressForShopLogic(self.request.shop)  # type:ignore
        address_for_shop.add_or_update_address(self.object)  # type:ignore
        return success_url

    def get_success_url(self):
        return reverse("smplshop.shop.master:choose_add_or_update_shop_details")


class ProductList(ListView):
    model = Product
    template_name = "shop/master/product_list.html"
    fields = ["code", "name", "price"]

    def get_verbose_field_name(self, field: str):
        return self.model._meta.get_field(field).verbose_name  # type: ignore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model"] = self.model
        context["fields"] = []
        for field in self.fields:
            context["fields"].append(self.get_verbose_field_name(field))
        context["fields"].append("Changed")
        return context


class AddProduct(CreateView):
    model = Product
    fields = ["code", "name", "price"]
    template_name = "shop/master/add_product.html"

    def get_success_url(self):
        return reverse("smplshop.shop.master:view_products")
