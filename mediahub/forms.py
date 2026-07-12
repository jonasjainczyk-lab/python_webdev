from django import forms
from .models import UserRating



class UserRatingForm(forms.ModelForm):
    rating = forms.DecimalField(min_value=0,max_value=10,max_digits=3,decimal_places=1,)

    class Meta:
        model = UserRating
        fields = ["rating", "text"]