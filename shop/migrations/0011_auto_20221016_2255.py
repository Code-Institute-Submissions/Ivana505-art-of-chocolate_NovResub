# Generated by Django 3.2 on 2022-10-16 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_buyer_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='chocolate_type',
        ),
        migrations.RemoveField(
            model_name='category',
            name='chocolate_name',
        ),
    ]
