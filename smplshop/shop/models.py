import uuid
from django.db.models import Model, CharField, UUIDField
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Address(Model):
    uuid = UUIDField(unique=True, default=uuid.uuid4, editable=False)

    name = CharField(
        verbose_name="Full name",
        max_length=1024,
    )

    address1 = CharField(
        verbose_name="Address line 1",
        max_length=1024,
    )

    address2 = CharField(
        verbose_name="Address line 2",
        max_length=1024,
    )

    zip_code = CharField(
        verbose_name="ZIP / Postal code",
        max_length=12,
    )

    city = CharField(
        verbose_name="City",
        max_length=1024,
    )

    country = CharField(
        verbose_name="Country",
        max_length=1024,
    )

    phone = CharField(
        verbose_name="Phone Number",
        validators=[RegexValidator(r"^[0-9]*$", _("Phone can only be numbers"))],
        max_length=10,
    )

    def __str__(self):
        return "{}-{}-{}".format(self.name, self.address1, self.zip_code)
