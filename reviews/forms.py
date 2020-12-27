from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    choices = ((1, '1 Star'), (2, '2 Stars'),
               (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars'))
    rating = forms.ChoiceField(choices=choices,
                                widget=forms.RadioSelect(attrs={
                                    'class': 'form-inline'}))

    class Meta:
        model = Review
        fields = ('title', 'content', 'rating')
