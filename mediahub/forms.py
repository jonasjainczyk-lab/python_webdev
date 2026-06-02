from django import forms
from .models import UserRating


RATING_CHOICES = [(i / 2, i / 2) for i in range(0, 21)]


class UserRatingForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=RATING_CHOICES)

    class Meta:
        model = UserRating
        fields = ["rating", "text"]