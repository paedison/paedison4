# Generated by Django 5.0.6 on 2024-05-27 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('a_psat', '0002_rename_collections_problem_collection_users_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problemcomment',
            name='tags',
        ),
    ]
