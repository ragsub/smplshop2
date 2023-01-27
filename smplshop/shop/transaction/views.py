from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.views.generic import ListView, View
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from .models import Order
from .logic import OrderLogic

# Create your views here.
class StoreOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name: str = "shop/transaction/orders.html"


class ChangeOrderStatus(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.order_uuid = request.GET.get("order_uuid", None)
        self.status_change = request.GET.get("change_status", None)
        return super().setup(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        order_logic = OrderLogic(order_uuid=self.order_uuid)
        try:
            order_logic.change_status(status_change=self.status_change)
        except ValidationError as e:
            messages.error(request, e.args[0])

        return redirect(reverse("smplshop.transaction:orders"))
