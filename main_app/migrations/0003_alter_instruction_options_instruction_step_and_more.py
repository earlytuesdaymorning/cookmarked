# Generated by Django 4.0.6 on 2022-07-13 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_remove_recipe_image_remove_recipe_instructions_photo_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instruction',
            options={'ordering': ['step']},
        ),
        migrations.AddField(
            model_name='instruction',
            name='step',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='label',
            field=models.CharField(max_length=150, verbose_name='Recipe Title'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='mealtype',
            field=models.CharField(max_length=100, verbose_name='Meal Type'),
        ),
    ]
