import uuid
from django.db.models import (
    ForeignKey,
    RESTRICT,
    CASCADE,
    CharField,
    UUIDField,
    FloatField,
    Model,
)
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from smplshop.users.tenant.models import TenantAwareAbstract
from smplshop.shop.models import Address

User = get_user_model()

# Create your models here.
class ShopDetails(TenantAwareAbstract):
    address = ForeignKey(Address, on_delete=RESTRICT)

    def __str__(self):
        return "{}-{}".format(self.shop, self.address)


class UserAddress(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    address = ForeignKey(Address, on_delete=RESTRICT)

    def __str__(self):
        return "{}-{}".format(self.user, self.address)


class Product(TenantAwareAbstract):
    uuid = UUIDField(unique=True, default=uuid.uuid4, editable=False)
    code = CharField(
        max_length=50,
        verbose_name="Product Code",
        blank=False,
        unique=True,
        validators=[
            RegexValidator(
                r"^[A-Za-z0-9_]+$",
                _("Product code can only be alphanumeric or underscore"),
            )
        ],
    )
    name = CharField(
        max_length=256, verbose_name="Product Name", blank=False, unique=True
    )
    price = FloatField(validators=[MinValueValidator(0.0)], verbose_name="Price")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("code", "name")
