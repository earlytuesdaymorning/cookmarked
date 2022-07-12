from dis import Instruction
from email.mime import image
from pyexpat import model
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
    # def __init__(self, label, image, mealtype, ingredients, instructions):
    label = models.CharField(max_length=150)
    # image = models.CharField(max_length=500)
    mealtype = models.CharField(max_length=100)
    ingredients = models.TextField(max_length=900)
    # instructions = models.TextField(max_length=1500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.label

class Instruction(models.Model):
    text = models.CharField(max_length=500)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return {self.text}

class Photo(models.Model):
    url = models.CharField(max_length=200)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for recipe_id: {self.recipe_id} @{self.url}"