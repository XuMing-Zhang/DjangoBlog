# Generated by Django 2.1.2 on 2018-11-08 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='enable',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
