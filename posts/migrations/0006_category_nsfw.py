# Generated by Django 3.1.7 on 2021-06-03 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20210602_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='NSFW',
            field=models.BooleanField(default=False),
        ),
    ]