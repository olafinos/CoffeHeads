from django import forms

from .models import Opinion


class OpinionForm(forms.ModelForm):
    rating = forms.FloatField(min_value=0.0,max_value=10.0)
    class Meta:
        model = Opinion
        fields = (
            "rating",
            "opinion",
            "acidity",
            "body",
            "flavor",
            "bitterness"
        )
