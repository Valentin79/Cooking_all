from random import random

from django.core.checks import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # для регистрации
from .models import Recipe, User, Category, Cooking_steps
from .forms import *
from django.views.generic.edit import UpdateView
from django import db # Для избежания ошибки "database is locked"


def home(request):
    recipe_list = {}
    recipes = Recipe.objects.order_by('?')[:5]
    for recipe in recipes:
        recipe_dict = {
            'title': recipe.title,
            'category': recipe.category.title,
            'description': recipe.description,
            'author': recipe.author,
            'image': recipe.image,
            'id': recipe.id,
            'visible': recipe.is_visible
        }
        recipe_list[f'Recipe_{recipe.id}'] = recipe_dict
    return render(request, 'home.html', context={"Recipes": recipe_list})


def view_all(request):
    recipe_list = {}
    recipes = Recipe.objects.all()
    for recipe in recipes:
        recipe_dict = {
            'title': recipe.title,
            'category': recipe.category.title,
            'description': recipe.description,
            'author': recipe.author,
            'image': recipe.image,
            'id': recipe.id,
            'visible': recipe.is_visible
        }
        recipe_list[f'Recipe_{recipe.id}'] = recipe_dict
    return render(request, 'view_all.html', context={"Recipes": recipe_list})


def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            fs = FileSystemStorage()
            fs.save(image.name, image)
            return render(request, 'upload_image.html', context={'title': 'успешно'})
    else:
        form = ImageForm()
        return render(request, 'upload_image.html', context={'form': form})


def about(request):
    return HttpResponse("About us")


def view_recipe(request, recipe_id):
    recipe = Recipe.objects.filter(pk=recipe_id).first()
    if recipe:
        all_cooking_steps = {
            '1': recipe.cooking_steps_key.step1,
            '2': recipe.cooking_steps_key.step2,
            '3': recipe.cooking_steps_key.step3,
            '4': recipe.cooking_steps_key.step4,
            '5': recipe.cooking_steps_key.step5,
            '6': recipe.cooking_steps_key.step6,
            '7': recipe.cooking_steps_key.step7,
            '8': recipe.cooking_steps_key.step8,
            '9': recipe.cooking_steps_key.step9,
            '10': recipe.cooking_steps_key.step10,
        }

        recipe_dict = {
            'title': recipe.title,
            'category': recipe.category.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'cooking_time': recipe.cooking_time,
            'cooking_steps': recipe.cooking_steps,
            'image': recipe.image,
            'author': recipe.author,
            'id': recipe_id,
            'visible': recipe.is_visible,
            'cooking_steps_new': all_cooking_steps,
        }

        db.connections.close_all()
        return render(request, 'view_recipe.html', context={'Dict': recipe_dict})
    return render(request, 'view_recipe.html', context={'message': 'рецепт не найден'})


def upload_recipe(request):
    if request.method == 'POST':
        form = UploadRecipeNew(request.POST, request.FILES)
        form2 = UploadCookingSteps(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            # Заполняем шаги приготовления
            step1 = form2.cleaned_data['step1']
            step2 = form2.cleaned_data['step2']
            step3 = form2.cleaned_data['step3']
            step4 = form2.cleaned_data['step4']
            step5 = form2.cleaned_data['step5']
            step6 = form2.cleaned_data['step6']
            step7 = form2.cleaned_data['step7']
            step8 = form2.cleaned_data['step8']
            step9 = form2.cleaned_data['step9']
            step10 = form2.cleaned_data['step10']
            # сохраняем шаги приготовления
            cooking_steps = Cooking_steps(
                step1=step1,
                step2=step2,
                step3=step3,
                step4=step4,
                step5=step5,
                step6=step6,
                step7=step7,
                step8=step8,
                step9=step9,
                step10=step10,
            )
            cooking_steps.save()

            # заполняем рецепт
            title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']
            ingredients = form.cleaned_data['ingredients']
            cooking_time = form.cleaned_data['cooking_time']
            image = form.cleaned_data['image']
            author_id = request.user.id
            category_id = Category.objects.get(title=category).pk
            cooking_steps_id = cooking_steps.pk
            # Сохраняем рецепт
            recipe = Recipe(
                title=title,
                category=Category(category_id),
                description=description,
                ingredients=ingredients,
                cooking_time=cooking_time,
                image=image.name,
                author=User(author_id),
                cooking_steps_key=Cooking_steps(cooking_steps_id)
            )
            recipe.save()
            fs = FileSystemStorage()
            fs.save(image.name, image)
            return redirect('view_recipe', recipe.pk)
        else:
            forms = {
                'recipe_form': form,
                'steps_form': form2
            }
            return render(request, 'upload_recipe.html', context={'forms': forms, 'message': 'Что-то не так'}, )
    else:
        recipe_form = UploadRecipeNew()
        steps_form = UploadCookingSteps()
        forms = {
            'recipe_form': recipe_form,
            'steps_form': steps_form
        }
        return render(request, 'upload_recipe.html', context={'forms': forms, 'message': 'Заполните форму'}, )


def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    cooking_steps = get_object_or_404(Cooking_steps, id=recipe.cooking_steps_key.id)
    if request.method == 'POST':
        form = EditRecipe(request.POST, request.FILES)
        form2 = UploadCookingSteps(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            recipe.title = form.cleaned_data['title']
            recipe.category.pk = form.cleaned_data['category']
            recipe.description = form.cleaned_data['description']
            recipe.ingredients = form.cleaned_data['ingredients']
            recipe.cooking_time = form.cleaned_data['cooking_time']

            cooking_steps.step1 = form2.cleaned_data['step1']
            cooking_steps.step2 = form2.cleaned_data['step2']
            cooking_steps.step3 = form2.cleaned_data['step3']
            cooking_steps.step4 = form2.cleaned_data['step4']
            cooking_steps.step5 = form2.cleaned_data['step5']
            cooking_steps.step6 = form2.cleaned_data['step6']
            cooking_steps.step7 = form2.cleaned_data['step7']
            cooking_steps.step8 = form2.cleaned_data['step8']
            cooking_steps.step9 = form2.cleaned_data['step9']
            cooking_steps.step10 = form2.cleaned_data['step10']
            recipe.save()
            cooking_steps.save()
            return redirect('view_recipe', recipe.pk)
        forms = {
            'recipe_form': form,
            'steps_form': form2
        }
        return render(request, 'upload_recipe.html', context={'forms': forms, 'message': 'Что-то пошло не так'}, )
    else:
        recipe_form = EditRecipe(instance=recipe)
        steps_form = UploadCookingSteps(instance=recipe.cooking_steps_key)
        forms = {
            'recipe_form': recipe_form,
            'steps_form': steps_form
        }
        return render(request, 'upload_recipe.html', context={'forms': forms, 'message': 'Отредактируйте форму'},)


def edit_image(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = EditImage(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            recipe.image = form.cleaned_data['image']
            recipe.save()
            fs = FileSystemStorage()
            fs.save(image.name, image)
            return redirect('view_recipe', recipe.pk)
        else:
            return render(request, 'upload_image.html', context={'form': form, 'message': 'Что-то не так'}, )
    else:
        form = EditImage()
        return render(request, 'upload_image.html', context={'form': form, 'message': 'Загрузите новое изображение'},)


def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    cooking_steps = get_object_or_404(Cooking_steps, id=recipe.cooking_steps_key.id)
    if request.method == 'GET':
        return render(request, 'recipe_confirm_delete.html', {'recipe': recipe})
    elif request.method == 'POST':
        recipe.delete()
        cooking_steps.delete() # Вообще это как то можно удалить на уровне модели, но у меня не работало. Разберусь позже.
        db.connections.close_all()
        return render(request, 'blank.html', context={'message': 'Запись удалена'})
    return redirect('home')


# =======================Register=======================================


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            return redirect('register_success')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required()
def profile(request):
    return render(request, 'profile.html')

#============================================================================

