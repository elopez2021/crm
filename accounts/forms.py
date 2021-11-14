from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
#Handling user creation form
from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        #it says go ahead and create a form with all the fields in the Order Model
class CreateUserForm(UserCreationForm):
     class Meta:
         model = User
         fields = ['username', 'email', 'password1', 'password2']
         #this is gonna give us a form with only these fields