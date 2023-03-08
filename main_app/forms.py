from django import forms
from.models import Item, TradeOffer

class InventoryForm(forms.Form):
    model = Item
    item_name = forms.CharField(max_length=100)

    def save(self):
        item = Item()
        item.item_name = self.cleaned_data['item_name']
        item.save()

class TradeOfferForm(forms.ModelForm):
    item_requested = forms.ModelChoiceField(
        queryset=Item.objects.none(),
        empty_label=None,
        widget=forms.RadioSelect,
        initial=None  # add this line to set initial value to None
    )

    class Meta:
        model = TradeOffer
        fields = ['item_requested', 'message']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.item_requested = kwargs.pop('item_requested')
        super().__init__(*args, **kwargs)
        self.fields['item_requested'].initial = None  # add this line to set initial value
