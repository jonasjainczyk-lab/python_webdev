from django import forms
from .models import UserRating


RATING_CHOICES = [(i / 2, i / 2) for i in range(0, 21)]


class UserRatingForm(forms.ModelForm):
    rating = forms.DecimalField(min_value=0,max_value=10,max_digits=3,decimal_places=1,)

    class Meta:
        model = UserRating
        fields = ["rating", "text"]