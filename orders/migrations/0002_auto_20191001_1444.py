# Generated by Django 2.0.3 on 2019-10-01 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='orders.Category')),
            ],
            options={
                'verbose_name_plural': 'Dishes',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=None, max_digits=4)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='orders.Dish')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='orders.Size'),
        ),
    ]
