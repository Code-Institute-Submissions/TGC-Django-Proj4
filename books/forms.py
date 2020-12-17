from django import forms
from .models import Book
from cloudinary.forms import CloudinaryJsFileField


class BookForm(forms.ModelForm):
    choices = ((1, '1 Star'), (2, '2 Stars'),
               (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars'))
    reviews = forms.ChoiceField(choices=choices,
                                widget=forms.RadioSelect(attrs={
                                    'class': 'form-inline'}))
    cover = CloudinaryJsFileField()

    class Meta:
        model = Book
        fields = ('__all__')

    

