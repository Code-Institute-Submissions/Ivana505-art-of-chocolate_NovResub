# Generated by Django 3.2 on 2022-09-19 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_chocolate_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='complete',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
