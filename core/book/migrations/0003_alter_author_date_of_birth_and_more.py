# Generated by Django 4.2 on 2024-08-17 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_remove_author_age_alter_author_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='date_of_birth',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='author',
            name='date_of_death',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
