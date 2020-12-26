from django import forms
from .models import Book, Genre, Tag
from cloudinary.forms import CloudinaryJsFileField


class BookForm(forms.ModelForm):
    choices = ((1, '1 Star'), (2, '2 Stars'),
               (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars'))
    reviews = forms.ChoiceField(choices=choices,
                                widget=forms.RadioSelect(attrs={
                                    'class': 'form-inline'}))
    cover = CloudinaryJsFileField()
    preview_1 = CloudinaryJsFileField()
    preview_2 = CloudinaryJsFileField()
    preview_3 = CloudinaryJsFileField()

    class Meta:
        model = Book
        fields = ('__all__')


class SearchForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=False)
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(), required=False)
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), required=False)
