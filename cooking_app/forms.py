from django import forms
from django.forms import ModelForm
from .models import Recipe, Category, Cooking_steps
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  # форма регистрации


class ImageForm(forms.Form):
    image = forms.ImageField()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UploadRecipe(forms.Form):  # первый вариант формы. Потом заменил ее на UploadRecipeNew(ModelForm):
    title = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'placeholder': 'Название'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    description = forms.CharField(max_length=400, widget=forms.Textarea(
        attrs={'placeholder': 'Краткое описание', 'rows': 5, 'cols': 43}))
    ingredients = forms.CharField(max_length=400, widget=forms.Textarea(
        attrs={'placeholder': 'Ингридиенты', 'rows': 5, 'cols': 43}))
    cooking_time = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'placeholder': '1 час'}))
    cooking_steps = forms.CharField(max_length=5000, widget=forms.Textarea(
        attrs={'placeholder': 'Порядок приготовления', 'rows': 10, 'cols': 43}))
    image = forms.ImageField()


class EditRecipe(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'category', 'description', 'ingredients', 'cooking_time']


class UploadRecipeNew(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'category', 'description', 'ingredients', 'cooking_time', 'image']


class UploadCookingSteps(ModelForm):
    class Meta:
        model = Cooking_steps
        fields = ['step1', 'step2', 'step3', 'step4', 'step5', 'step6', 'step7', 'step8', 'step9', 'step10']


class EditImage(ModelForm):
    class Meta:
        model = Recipe
        fields = ['image']
