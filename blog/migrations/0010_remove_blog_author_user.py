# Generated by Django 2.1.2 on 2018-11-09 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_blog_author_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='author_user',
        ),
    ]
