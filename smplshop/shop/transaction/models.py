import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import (
    Model,
    ForeignKey,
    RESTRICT,
    CASCADE,
    PROTECT,
    UUIDField,
    IntegerField,
    DateTimeField,
    CharField,
    FloatField,
)
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from smplshop.shop.models import Address
from smplshop.shop.master.models import Product
from smplshop.users.tenant.models import TenantAwareAbstract

User = get_user_model()

# Create your models here.
class Cart(TenantAwareAbstract):
    uuid = UUIDField(unique=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.uuid) + "-" + str(self.shop)

    @property
    def total_cart_price(self):
        return "%s" % (sum([float(obj.total_price) for obj in self.cartitem_set.all()]))  # type: ignore


class CartItem(Model):
    uuid = UUIDField(unique=True, default=uuid.uuid4, editable=False)
    cart = ForeignKey(to=Cart, on_delete=CASCADE, verbose_name="Cart For")
    product = ForeignKey(
        to=Product,
        on_delete=CASCADE,
        verbose_name="Product",
    )
    quantity = IntegerField(
        validators=[MinValueValidator(0.0)],
        verbose_name="Quanity",
        default=0,
    )

    class Meta:
        UniqueConstraint(fields=["cart", "product"], name="unique_cart_product")

    def __str__(self):
        return str(self.cart) + "-" + str(self.product)

    @property
    def total_price(self):
        return "%s" % (self.product.price * self.quantity)  # type: ignore


class Order(TenantAwareAbstract):

    ORDER_STATUS_CHOICES = [
        ("placed", "Order Placed"),
        ("accepted", "Order Accepted"),
        ("shipped", "Order Shipped"),
        ("delivered", "Order Delivered"),
        ("closed", "Order Closed"),
        ("cancelled", "Order Cancelled"),
    ]
    uuid = UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = ForeignKey(to=User, on_delete=CASCADE)
    address = ForeignKey(Address, on_delete=RESTRICT)
    status = CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default="placed")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def can_shop_cancel_order(self):
        return True if self.status in ["placed", "accepted", "shipped"] else False

    def cancel_order(self):
        if self.can_shop_cancel_order():
            self.status = "cancelled"
        else:
            raise ValidationError(
                _("{}{}{}".format("Order ", self.uuid, " cannot be cancelled"))
            )
        self.save()

    def can_shop_ship_order(self):
        return True if self.status == "accepted" else False

    def ship_order(self):
        if self.can_shop_ship_order():
            self.status = "shipped"
        else:
            raise ValidationError(
                _("{}{}{}".format("Order ", self.uuid, " cannot be shipped"))
            )
        self.save()

    def can_shop_accept_order(self):
        return True if self.status == "placed" else False

    def accept_order(self):
        if self.can_shop_accept_order():
            self.status = "accepted"
        else:
            raise ValidationError(
                _("{}{}{}".format("Order ", self.uuid, " cannot be accepted"))
            )
        self.save()

    def can_shop_deliver_order(self):
        return True if self.status == "shipped" else False

    def deliver_order(self):
        if self.can_shop_deliver_order():
            self.status = "delivered"
        else:
            raise ValidationError(
                _("{}{}{}".format("Order ", self.uuid, " cannot be delivered"))
            )
        self.save()

    def can_shop_close_order(self):
        return True if self.status == "delivered" else False

    def close_order(self):
        if self.can_shop_close_order():
            self.status = "closed"
        else:
            raise ValidationError(
                _("{}{}{}".format("Order ", self.uuid, " cannot be closed"))
            )
        self.save()

    @property
    def total_order_price(self):
        return sum([float(obj.total_price) for obj in self.orderitem_set.all()])  # type: ignore

    class Meta:
        ordering = ("shop", "-created_at", "-updated_at")


class OrderItem(Model):
    order = ForeignKey(to=Order, on_delete=CASCADE)
    product = ForeignKey(to=Product, on_delete=PROTECT)
    price = FloatField(validators=[MinValueValidator(0.0)])
    quantity = IntegerField(validators=[MinValueValidator(0)])

    @property
    def total_price(self):
        return self.price * self.quantity  # type: ignore
