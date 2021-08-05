from django import forms

class ListingForm(forms.Form):
    CLOTHING = 'CL'
    ELECTRONICS = 'EL'
    BOOKS = 'BK'
    GROCERIES = 'GR'
    FOOTWEAR = 'FT'
    PLANTS = 'PL'
    STATIONARY = 'ST'
    OTHER = 'OT'
    name = forms.CharField(label='your_name', max_length=240)
    price  = forms.IntegerField(min_value=0)
    image = forms.URLField()
    category = forms.ChoiceField(choices=[
        (CLOTHING, 'Clothing'),
        (ELECTRONICS, 'Electronics'),
        (BOOKS, 'Books'),
        (GROCERIES, 'Groceries'),
        (FOOTWEAR, 'Footwear'),
        (PLANTS, 'Plants'),
        (STATIONARY, 'Stationary'),
        (OTHER, 'Other')
    ])


class BidsForm(forms.Form):
    bid = forms.IntegerField(min_value=0, label='Bid')
