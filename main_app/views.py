from cProfile import label
from dataclasses import field
from email.mime import image
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import is_valid_path
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import uuid
import boto3
from .models import Recipe, Instruction, Photo
from .forms import InstructionForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'cookmarked'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def all_recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/all.html', { 'recipes': recipes })

def cookmarked_recipes(request):
    myrecipes = Recipe.objects.filter(user=request.user)
    return render(request, 'recipes/index.html', { 'myrecipes': myrecipes })

def recipe_details(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    instruction_form = InstructionForm()
    return render(request, 'recipes/details.html', {
        'recipe': recipe,
        'instruction_form': instruction_form
    })

def my_recipe_details(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    instruction_form = InstructionForm()
    return render(request, 'recipes/mydetails.html', {
        'recipe': recipe,
        'instruction_form': instruction_form
    })

def add_instruction(request, recipe_id):
    form = InstructionForm(request.POST)
    if form.is_valid():
        new_instuction = form.save(commit=False)
        new_instuction.recipe_id = recipe_id
        new_instuction.save()
    return redirect('mydetails', recipe_id=recipe_id)

def add_photo(request, recipe_id):
    photo_file = request.FILES.get('photo-file', None)

    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, recipe_id=recipe_id)
            photo.save()
        except Exception as error:
            print('An error occurred uploading file to S3: ', error)
    return redirect('mydetails', recipe_id=recipe_id)

class RecipeCreate(CreateView):
    model = Recipe
    fields = ['label', 'mealtype', 'ingredients']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class YourRecipeCreate(CreateView):
    model = Recipe
    fields = ['label', 'mealtype', 'ingredients']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RecipeUpdate(UpdateView):
    model = Recipe
    fields = ['label', 'mealtype', 'ingredients']

class RecipeDelete(DeleteView):
    model = Recipe
    success_url = '/cookmarked/'






# class Recipe:
#     def __init__(self, label, image, mealtype, ingredients, instructions):
#         self.label = label
#         self.image = image
#         self.mealtype = mealtype
#         self.ingredients = ingredients
#         self.instructions = instructions

# recipes = [
#     Recipe(
#         'Chicken And Dumplings',
#         'https://edamam-product-images.s3.amazonaws.com/web-img/51e/51ec6da33b8078114bf995d4b5d2a682-m.JPG?X-Amz-Security-Token=IQoJb3JpZ2luX2VjECoaCXVzLWVhc3QtMSJIMEYCIQCQGmRu9A4LArLFkvf9cfsuKz8lLJFpm%2Bf8o8QdsIfisQIhAMH45LkKNtSgCtxqMBm6tH132TkxIoAT%2BgxWRHqayx%2BHKtIECGIQABoMMTg3MDE3MTUwOTg2IgxFa%2FnH7lngwDaI9bEqrwQvdYjl%2BHRijSZRt%2B2GCSRhLjFi9SLhXSmJTsLwabKH0ZtaZEWYXmRktTguMzsXr%2BrBI8Ao%2BTnWyiypOu2lQWbRxIejhv56QWXS1qVaDtYczqovKXgzp4AyYoVOmIi1tcRc%2BUzSLMBIhU2LKN5pd420kPw0gEhZ9e7Nd6tD1npEiZbBwHtjfu43f4k1PmH7kAzkwyMQAtO7pAuwC4PVA5Crd%2B6DOmuHGDwsTx22waAWYe3u62bI%2Fec5faJGay%2B3nM29qkvw9%2FkkjF6VkgyhqJCqcBSBVa7bF2%2BHHCRCA65pHMDNNXhaGZiYkq0AWKj4tJgvKzB%2BrwgQZLboBPIQXAk6WwnHHu12Y1ZmPUprzJv6%2BgnqPU6VhqvNCUeAmH3c%2FAGSvSh7a8h6lrLt2W68INGuRn07DWXPYK7UFfiVT%2FId0bx8Jrpp7DtxgXsNuP0yA%2F%2F2PJoHytCHmL9ROtH5TCBu1jLQkOrvVhMnDSpTjabRV3%2F00dpWEQJaHGpIyYmD1ejvz4GUV8w6Y4Ltautq%2BD61AOebqex058XPKmqdewPO87FqIvkEhj6EFL6tmZ%2B7qmwDhHEev2yFOmQfCCsk9c7iA5%2FZV%2BuQRNSOD3Fuv%2Fr6G4WgfeplKclWjrlWMrgworMcvCLEhTBPOSQ8JzFf%2F0FLdEwSlzYsC7d26dz9tEz%2Fju%2BqBB8eusnLVP7T%2BHSmaAiO42JUnMQ0M16nW%2Frwu34ZjyPd3mb7AgRgYDqAS8NwMKLbtpYGOqgBDkZ9nqaQPN5YhTFt50cDdHfUGDfA5xsSYwd3MhDirBjeINhN9hTc8SWUSorxGRU3b1V5B8rOdInFoXCXw9na7wJPGsp2b%2BuQTRde%2FmM0eMUlFZY6%2BKbiRvQ2wVs5ZH%2FuqKNwz%2FTq6aNqZgvwyixoHuICsbZzMAHTAn9iBLFfoRsopTrFcjGzUSZL3J4wy2CVyubCyiECdEdFBOocEaOyFwodiVyZGBT8&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220712T183018Z&X-Amz-SignedHeaders=host&X-Amz-Expires=3600&X-Amz-Credential=ASIASXCYXIIFOKJKIB6H%2F20220712%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=b1d961385287750f9d4832d7b4d3162f03f968eca3c34a0042d373757c088f21',
#         'dinner',
#         """
#         1 whole chicken,
#         6 cups flour,
#         1 1/2 cup self-rising flour,
#         3/4 cups shortening,
#         3 cups whole milk
#         """,
#         """
#         1. Rinse chicken and place in a 10 quart pot.,
#         2. Fill pot with water and bring to a boil.,
#         3. Cook until chicken reaches internal temperature of 165 degrees F.,
#         4. Remove chicken from the broth and de-bone and then return chicken to the broth.,
#         5. In a mixing bowl, add flour, self-rising flour, shortening and milk. Mix and knead dough.,
#         6. Roll out dough, adding flour as needed. Cut into 2" X 2" squares.,
#         7. Bring chicken and broth to a rolling boil.,
#         8. Place squares individually into broth and chicken, then boil for 20 minutes, stirring occasionally.
#         """
#     ),
#     Recipe(
#         'Chikeen nope',
#         'https://edamam-product-images.s3.amazonaws.com/web-img/51e/51ec6da33b8078114bf995d4b5d2a682-m.JPG?X-Amz-Security-Token=IQoJb3JpZ2luX2VjECoaCXVzLWVhc3QtMSJIMEYCIQCQGmRu9A4LArLFkvf9cfsuKz8lLJFpm%2Bf8o8QdsIfisQIhAMH45LkKNtSgCtxqMBm6tH132TkxIoAT%2BgxWRHqayx%2BHKtIECGIQABoMMTg3MDE3MTUwOTg2IgxFa%2FnH7lngwDaI9bEqrwQvdYjl%2BHRijSZRt%2B2GCSRhLjFi9SLhXSmJTsLwabKH0ZtaZEWYXmRktTguMzsXr%2BrBI8Ao%2BTnWyiypOu2lQWbRxIejhv56QWXS1qVaDtYczqovKXgzp4AyYoVOmIi1tcRc%2BUzSLMBIhU2LKN5pd420kPw0gEhZ9e7Nd6tD1npEiZbBwHtjfu43f4k1PmH7kAzkwyMQAtO7pAuwC4PVA5Crd%2B6DOmuHGDwsTx22waAWYe3u62bI%2Fec5faJGay%2B3nM29qkvw9%2FkkjF6VkgyhqJCqcBSBVa7bF2%2BHHCRCA65pHMDNNXhaGZiYkq0AWKj4tJgvKzB%2BrwgQZLboBPIQXAk6WwnHHu12Y1ZmPUprzJv6%2BgnqPU6VhqvNCUeAmH3c%2FAGSvSh7a8h6lrLt2W68INGuRn07DWXPYK7UFfiVT%2FId0bx8Jrpp7DtxgXsNuP0yA%2F%2F2PJoHytCHmL9ROtH5TCBu1jLQkOrvVhMnDSpTjabRV3%2F00dpWEQJaHGpIyYmD1ejvz4GUV8w6Y4Ltautq%2BD61AOebqex058XPKmqdewPO87FqIvkEhj6EFL6tmZ%2B7qmwDhHEev2yFOmQfCCsk9c7iA5%2FZV%2BuQRNSOD3Fuv%2Fr6G4WgfeplKclWjrlWMrgworMcvCLEhTBPOSQ8JzFf%2F0FLdEwSlzYsC7d26dz9tEz%2Fju%2BqBB8eusnLVP7T%2BHSmaAiO42JUnMQ0M16nW%2Frwu34ZjyPd3mb7AgRgYDqAS8NwMKLbtpYGOqgBDkZ9nqaQPN5YhTFt50cDdHfUGDfA5xsSYwd3MhDirBjeINhN9hTc8SWUSorxGRU3b1V5B8rOdInFoXCXw9na7wJPGsp2b%2BuQTRde%2FmM0eMUlFZY6%2BKbiRvQ2wVs5ZH%2FuqKNwz%2FTq6aNqZgvwyixoHuICsbZzMAHTAn9iBLFfoRsopTrFcjGzUSZL3J4wy2CVyubCyiECdEdFBOocEaOyFwodiVyZGBT8&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220712T183018Z&X-Amz-SignedHeaders=host&X-Amz-Expires=3600&X-Amz-Credential=ASIASXCYXIIFOKJKIB6H%2F20220712%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=b1d961385287750f9d4832d7b4d3162f03f968eca3c34a0042d373757c088f21',
#         'dinner',
#         """
#         1 whole filler,
#         6 cups flour,
#         1 1/2 cup self-rising flour,
#         3/4 cups shortening,
#         3 cups whole fillers
#         """,
#         """
#         1. Rinse chicken and place in a 10 quart WHAT.,
#         2. Fill pot with water and bring to a boil.,
#         3. Cook until chicken reaches internal temperature of 165 degrees F.,
#         4. Remove chicken from the broth and de-bone and then return chicken to the broth.,
#         5. In a mixing bowl, add flour, self-rising flour, shortening and milk. Mix and knead dough.,
#         6. Remove instructions for fun.
#         """
#     )
# ]

# myrecipes = [
#     Recipe(
#         'MY Chicken And Dumplings',
#         'https://edamam-product-images.s3.amazonaws.com/web-img/51e/51ec6da33b8078114bf995d4b5d2a682-m.JPG?X-Amz-Security-Token=IQoJb3JpZ2luX2VjECoaCXVzLWVhc3QtMSJIMEYCIQCQGmRu9A4LArLFkvf9cfsuKz8lLJFpm%2Bf8o8QdsIfisQIhAMH45LkKNtSgCtxqMBm6tH132TkxIoAT%2BgxWRHqayx%2BHKtIECGIQABoMMTg3MDE3MTUwOTg2IgxFa%2FnH7lngwDaI9bEqrwQvdYjl%2BHRijSZRt%2B2GCSRhLjFi9SLhXSmJTsLwabKH0ZtaZEWYXmRktTguMzsXr%2BrBI8Ao%2BTnWyiypOu2lQWbRxIejhv56QWXS1qVaDtYczqovKXgzp4AyYoVOmIi1tcRc%2BUzSLMBIhU2LKN5pd420kPw0gEhZ9e7Nd6tD1npEiZbBwHtjfu43f4k1PmH7kAzkwyMQAtO7pAuwC4PVA5Crd%2B6DOmuHGDwsTx22waAWYe3u62bI%2Fec5faJGay%2B3nM29qkvw9%2FkkjF6VkgyhqJCqcBSBVa7bF2%2BHHCRCA65pHMDNNXhaGZiYkq0AWKj4tJgvKzB%2BrwgQZLboBPIQXAk6WwnHHu12Y1ZmPUprzJv6%2BgnqPU6VhqvNCUeAmH3c%2FAGSvSh7a8h6lrLt2W68INGuRn07DWXPYK7UFfiVT%2FId0bx8Jrpp7DtxgXsNuP0yA%2F%2F2PJoHytCHmL9ROtH5TCBu1jLQkOrvVhMnDSpTjabRV3%2F00dpWEQJaHGpIyYmD1ejvz4GUV8w6Y4Ltautq%2BD61AOebqex058XPKmqdewPO87FqIvkEhj6EFL6tmZ%2B7qmwDhHEev2yFOmQfCCsk9c7iA5%2FZV%2BuQRNSOD3Fuv%2Fr6G4WgfeplKclWjrlWMrgworMcvCLEhTBPOSQ8JzFf%2F0FLdEwSlzYsC7d26dz9tEz%2Fju%2BqBB8eusnLVP7T%2BHSmaAiO42JUnMQ0M16nW%2Frwu34ZjyPd3mb7AgRgYDqAS8NwMKLbtpYGOqgBDkZ9nqaQPN5YhTFt50cDdHfUGDfA5xsSYwd3MhDirBjeINhN9hTc8SWUSorxGRU3b1V5B8rOdInFoXCXw9na7wJPGsp2b%2BuQTRde%2FmM0eMUlFZY6%2BKbiRvQ2wVs5ZH%2FuqKNwz%2FTq6aNqZgvwyixoHuICsbZzMAHTAn9iBLFfoRsopTrFcjGzUSZL3J4wy2CVyubCyiECdEdFBOocEaOyFwodiVyZGBT8&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220712T183018Z&X-Amz-SignedHeaders=host&X-Amz-Expires=3600&X-Amz-Credential=ASIASXCYXIIFOKJKIB6H%2F20220712%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=b1d961385287750f9d4832d7b4d3162f03f968eca3c34a0042d373757c088f21',
#         'dinner',
#         """
#         1 whole chicken,
#         6 cups flour,
#         1 1/2 cup self-rising flour,
#         3/4 cups shortening,
#         3 cups whole milk
#         """,
#         """
#         1. Rinse chicken and place in a 10 quart pot.,
#         2. Fill pot with water and bring to a boil.,
#         3. Cook until chicken reaches internal temperature of 165 degrees F.,
#         4. Remove chicken from the broth and de-bone and then return chicken to the broth.,
#         5. In a mixing bowl, add flour, self-rising flour, shortening and milk. Mix and knead dough.,
#         6. Roll out dough, adding flour as needed. Cut into 2" X 2" squares.,
#         7. Bring chicken and broth to a rolling boil.,
#         8. Place squares individually into broth and chicken, then boil for 20 minutes, stirring occasionally.
#         """
#     ),
#     Recipe(
#         'MY Chikeen nope',
#         'https://edamam-product-images.s3.amazonaws.com/web-img/51e/51ec6da33b8078114bf995d4b5d2a682-m.JPG?X-Amz-Security-Token=IQoJb3JpZ2luX2VjECoaCXVzLWVhc3QtMSJIMEYCIQCQGmRu9A4LArLFkvf9cfsuKz8lLJFpm%2Bf8o8QdsIfisQIhAMH45LkKNtSgCtxqMBm6tH132TkxIoAT%2BgxWRHqayx%2BHKtIECGIQABoMMTg3MDE3MTUwOTg2IgxFa%2FnH7lngwDaI9bEqrwQvdYjl%2BHRijSZRt%2B2GCSRhLjFi9SLhXSmJTsLwabKH0ZtaZEWYXmRktTguMzsXr%2BrBI8Ao%2BTnWyiypOu2lQWbRxIejhv56QWXS1qVaDtYczqovKXgzp4AyYoVOmIi1tcRc%2BUzSLMBIhU2LKN5pd420kPw0gEhZ9e7Nd6tD1npEiZbBwHtjfu43f4k1PmH7kAzkwyMQAtO7pAuwC4PVA5Crd%2B6DOmuHGDwsTx22waAWYe3u62bI%2Fec5faJGay%2B3nM29qkvw9%2FkkjF6VkgyhqJCqcBSBVa7bF2%2BHHCRCA65pHMDNNXhaGZiYkq0AWKj4tJgvKzB%2BrwgQZLboBPIQXAk6WwnHHu12Y1ZmPUprzJv6%2BgnqPU6VhqvNCUeAmH3c%2FAGSvSh7a8h6lrLt2W68INGuRn07DWXPYK7UFfiVT%2FId0bx8Jrpp7DtxgXsNuP0yA%2F%2F2PJoHytCHmL9ROtH5TCBu1jLQkOrvVhMnDSpTjabRV3%2F00dpWEQJaHGpIyYmD1ejvz4GUV8w6Y4Ltautq%2BD61AOebqex058XPKmqdewPO87FqIvkEhj6EFL6tmZ%2B7qmwDhHEev2yFOmQfCCsk9c7iA5%2FZV%2BuQRNSOD3Fuv%2Fr6G4WgfeplKclWjrlWMrgworMcvCLEhTBPOSQ8JzFf%2F0FLdEwSlzYsC7d26dz9tEz%2Fju%2BqBB8eusnLVP7T%2BHSmaAiO42JUnMQ0M16nW%2Frwu34ZjyPd3mb7AgRgYDqAS8NwMKLbtpYGOqgBDkZ9nqaQPN5YhTFt50cDdHfUGDfA5xsSYwd3MhDirBjeINhN9hTc8SWUSorxGRU3b1V5B8rOdInFoXCXw9na7wJPGsp2b%2BuQTRde%2FmM0eMUlFZY6%2BKbiRvQ2wVs5ZH%2FuqKNwz%2FTq6aNqZgvwyixoHuICsbZzMAHTAn9iBLFfoRsopTrFcjGzUSZL3J4wy2CVyubCyiECdEdFBOocEaOyFwodiVyZGBT8&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220712T183018Z&X-Amz-SignedHeaders=host&X-Amz-Expires=3600&X-Amz-Credential=ASIASXCYXIIFOKJKIB6H%2F20220712%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=b1d961385287750f9d4832d7b4d3162f03f968eca3c34a0042d373757c088f21',
#         'dinner',
#         """
#         1 whole filler,
#         6 cups flour,
#         1 1/2 cup self-rising flour,
#         3/4 cups shortening,
#         3 cups whole fillers
#         """,
#         """
#         1. Rinse chicken and place in a 10 quart WHAT.,
#         2. Fill pot with water and bring to a boil.,
#         3. Cook until chicken reaches internal temperature of 165 degrees F.,
#         4. Remove chicken from the broth and de-bone and then return chicken to the broth.,
#         5. In a mixing bowl, add flour, self-rising flour, shortening and milk. Mix and knead dough.,
#         6. Remove instructions for fun.
#         """
#     )
# ]