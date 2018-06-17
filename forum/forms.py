from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Thread, Post


class MySignUpForm(UserCreationForm):
    # imie_i_nazwisko = forms.CharField(max_length=100, required=False, help_text='Nie wymagane')
    first_name = forms.CharField(label='Imię', max_length=100, required=False, help_text='Nie wymagane')
    last_name = forms.CharField(label='Nazwisko', max_length=100, required=False, help_text='Nie wymagane')
    email = forms.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(MySignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = 'Maksymalnie 150 znaków. Jedynie litery, cyfry i @/./+/-/_.'
        self.fields['password1'].help_text = 'Twoje hasło musi zawierać co najmniej 8 znaków. '


class ThreadForm(forms.ModelForm):

    class Meta:
        model = Thread
        fields = {'category_name', 'title', 'description'}

    def __init__(self, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['style'] = 'width:800px; height:150px'
        self.fields['title'].widget.attrs['style'] = 'width:600px; height:25px'
        self.fields['category_name'].widget.attrs['style'] = 'width:300px; height:25px'
        self.fields.keyOrder = ['title', 'category_name', 'description']
        self.fields['category_name'].label = 'Kategoria'
        self.fields['title'].label = 'Tytuł'
        self.fields['description'].label = 'Opis'


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = {'text'}

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = 'Komentarz'
        self.fields['text'].widget.attrs['cols'] = 100
        self.fields['text'].widget.attrs['rows'] = 15


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False, max_length=150)
    # imie_i_nazwisko = forms.CharField(required=False)
    first_name = forms.CharField(label='Imię', max_length=100, required=False, help_text='Nie wymagane')
    last_name = forms.CharField(label='Nazwisko', max_length=100, required=False, help_text='Nie wymagane')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
