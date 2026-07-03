from django import forms
from .models import UserRating

class UserRatingForm(forms.ModelForm):
    rating = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': '0',
            'max': '10',
            'step': '0.5',
            'class': 'form-range',
            'id': 'ratingSlider'
        })
    )

    class Meta:
        model = UserRating
        fields = ["rating", "text"]