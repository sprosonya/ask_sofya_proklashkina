# Generated by Django 4.2.13 on 2024-06-18 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_profile_alter_answer_author_alter_question_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tag',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
