from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.title}'


class Cooking_steps(models.Model):
    step1 = models.TextField(max_length=500)
    image_step1 = models.ImageField(null=True)
    step2 = models.TextField(blank=True, max_length=500)
    image_step2 = models.ImageField(null=True)
    step3 = models.TextField(blank=True, max_length=500)
    image_step3 = models.ImageField(null=True)
    step4 = models.TextField(blank=True, max_length=500)
    image_step4 = models.ImageField(null=True)
    step5 = models.TextField(blank=True, max_length=500)
    image_step5 = models.ImageField(null=True)
    step6 = models.TextField(blank=True, max_length=500)
    image_step6 = models.ImageField(null=True)
    step7 = models.TextField(blank=True, max_length=500)
    image_step7 = models.ImageField(null=True)
    step8 = models.TextField(blank=True, max_length=500)
    image_step8 = models.ImageField(null=True)
    step9 = models.TextField(blank=True, max_length=500)
    image_step9 = models.ImageField(null=True)
    step10 = models.TextField(blank=True, max_length=500)
    image_step10 = models.ImageField(null=True)

    def __str__(self):
        return f'{self.step1}, {self.step2}, {self.step3}'


class Recipe(models.Model):
    title = models.CharField(max_length=40)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    description = models.TextField(max_length=400)
    ingredients = models.TextField(max_length=400)
    cooking_time = models.CharField(max_length=40)
    cooking_steps = models.TextField(max_length=5000)
    image = models.ImageField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)
    publishing_date = models.DateField(default=datetime.today())
    cooking_steps_key = models.ForeignKey(Cooking_steps, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, {self.category}, {self.author}'
