from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CharField,
    ManyToManyField,
    ForeignKey,
    Model,
    CASCADE,
    OneToOneField,
    EmailField,
    BooleanField,
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .tenant.models import Shop


class User(AbstractUser):
    """
    Default custom user model for SmplShop.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    USERNAME_FIELD = "email"

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    shop = ManyToManyField(to=Shop, through="UsertoShop", blank=True)
    username = CharField(
        _("username"),
        max_length=150,
        unique=False,
        blank=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
    )
    email = EmailField(
        _("email address"),
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    REQUIRED_FIELDS = ["username"]

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"email": self.email})


class UserToShop(Model):
    ROLES = [
        (_("owner"), _("Store Owner")),
        (_("manager"), _("Store Manager")),
        (_("shipper"), _("Store Delivery")),
        (_("buyer"), _("Store Buyer")),
    ]

    shop = ForeignKey(
        to=Shop,
        on_delete=CASCADE,
    )
    user = ForeignKey(to=User, on_delete=CASCADE)

    role = CharField(
        verbose_name=_("Role"), max_length=20, choices=ROLES, default="buyer"
    )

    class Meta:
        ordering = ("role",)

    def __str__(self):
        return "{}{}{}".format(self.user, "-", self.shop)


class CurrentShopForUser(Model):
    user = OneToOneField(to=User, on_delete=CASCADE)
    shop = ForeignKey(
        to=Shop,
        on_delete=CASCADE,
    )

    class Meta:
        ordering = ("user", "shop")

    def __str__(self):
        return "{}{}{}".format(self.user, "-", self.shop)
