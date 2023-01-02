from django.forms import Form, ModelChoiceField
from .master.logic import AddressForUserLogic


class SelectAddressForm(Form):
    address = ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop("addresses")
        super().__init__(*args, **kwargs)
        if qs is not None:
            self.fields["address"].queryset = qs
