from django.urls import path

from .views import StoreOrderListView, ChangeOrderStatus

app_name = "smplshop.transaction"
urlpatterns = [
    path("orders/", view=StoreOrderListView.as_view(), name="orders"),
    path("order/status", view=ChangeOrderStatus.as_view(), name="change_order_status"),
]
