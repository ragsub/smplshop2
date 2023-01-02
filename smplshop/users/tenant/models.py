from django.db.models import Model, CharField, ForeignKey, CASCADE
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from .utils import state
from .managers import TenantManager

# Create your models here.


class Shop(Model):
    code = CharField(
        verbose_name=_("Shop Code"),
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                r"^[A-Za-z0-9_]+$",
                _("Shop code can only be alphanumeric or underscore"),
            )
        ],
    )
    name = CharField(verbose_name=_("Shop Name"), max_length=50)

    class Meta:
        ordering = ("code", "name")

    def __str__(self):
        return self.name


class TenantAwareAbstract(Model):
    """Abstract model that implements the model save defining a tenant"""

    shop = ForeignKey(Shop, on_delete=CASCADE)

    objects = TenantManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Set tenant field on save"""
        setattr(self, "shop", state.get_current_tenant())

        super().save(*args, **kwargs)

    def get_tenant_instance(self):
        """Returns the model's tenant instance"""
        return getattr(self, "shop")
