# Generated by Django 3.2 on 2022-09-17 23:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('zipcode', models.CharField(max_length=255)),
                ('date_added', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=255)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChocolateItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(max_length=150, null=True)),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.buyer')),
            ],
        ),
        migrations.AlterModelOptions(
            name='chocolate',
            options={},
        ),
        migrations.RemoveField(
            model_name='chocolate',
            name='author',
        ),
        migrations.RemoveField(
            model_name='chocolate',
            name='category',
        ),
        migrations.RemoveField(
            model_name='chocolate',
            name='created',
        ),
        migrations.RemoveField(
            model_name='chocolate',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='chocolate',
            name='description',
        ),
        migrations.RemoveField(
            model_name='chocolate',
            name='image',
        ),
        migrations.RemoveField(
            model_name='chocolate',
            name='in_stock',
        ),
        migrations.RemoveField(
            model_name='chocolate',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='chocolate',
            name='updated',
        ),
        migrations.AddField(
            model_name='chocolate',
            name='digital',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='chocolate',
            name='price',
            field=models.FloatField(),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AddField(
            model_name='chocolateitem',
            name='chocolate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.chocolate'),
        ),
        migrations.AddField(
            model_name='chocolateitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.order'),
        ),
        migrations.AddField(
            model_name='address',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.buyer'),
        ),
        migrations.AddField(
            model_name='address',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.order'),
        ),
    ]
