#
# forms.py
#

from django import forms

from zombie.models import FoodEntry


class FoodForm(forms.Form):
    image = forms.ImageField()
    food_type = forms.ChoiceField(
        choices=FoodEntry.DISH_CHOICES,
        widget=forms.RadioSelect
    )

