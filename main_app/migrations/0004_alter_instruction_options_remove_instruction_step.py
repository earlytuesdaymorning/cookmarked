# Generated by Django 4.0.6 on 2022-07-13 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_instruction_options_instruction_step_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instruction',
            options={},
        ),
        migrations.RemoveField(
            model_name='instruction',
            name='step',
        ),
    ]
