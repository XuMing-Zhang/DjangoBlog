# Generated by Django 2.1.2 on 2018-11-09 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_contact_captcha'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='captcha',
            field=models.CharField(default=1234, max_length=8, verbose_name='验证码'),
            preserve_default=False,
        ),
    ]