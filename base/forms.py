from django import forms
from .models import Product, User, Comment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'location', 'phonenumber', 'avatar']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'bio' ,'location', 'phonenumber', 'avatar']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class ProductForm(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))
    
    class Meta:
        model = Product
        exclude = ('category','advertiser')
        fields = ['category', 'name', 'description', 'location', 'condition', 'price', 'geartype', 'motortype', 'year', 'color', 'num_rooms', 'num_baths', 'images', 'advertiser']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.category:
            category_name = instance.category.name

            if category_name == 'Cars':
                self.fields['motortype'] = forms.CharField(label='Motortype', required=True)
                self.fields['geartype'] = forms.CharField(label='Geartype', required=True)
                self.fields['year'] = forms.IntegerField(label='Year', required=True)
                self.fields['color'] = forms.CharField(label='Color', required=True)
            elif category_name == 'Home':
                self.fields['num_rooms'] = forms.IntegerField(label='Number of Rooms', required=True)
                self.fields['num_baths'] = forms.IntegerField(label='Number of Baths', required=True)

