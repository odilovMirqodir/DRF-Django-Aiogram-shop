# Generated by Django 5.0.3 on 2024-03-23 14:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=30, unique=True, verbose_name='Kategoriya nomi')),
            ],
            options={
                'verbose_name': 'Kategoriya',
                'verbose_name_plural': 'Kategoriyalar',
            },
        ),
        migrations.CreateModel(
            name='ExcelFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='excel_files/', verbose_name='Excel Fayl')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.TextField()),
                ('customer_phone', models.CharField(max_length=50)),
                ('customer_user_name', models.CharField(max_length=120)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Zakazchi',
                'verbose_name_plural': 'Zakazchilar',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.BigIntegerField(null=True, unique=True, verbose_name='Foydalanuvchi ID')),
                ('username', models.CharField(max_length=50, null=True, verbose_name='Foydalanuvchi username')),
                ('user_full_name', models.CharField(max_length=25, null=True, verbose_name='Foydalanuvchi Ismi Familyasi')),
                ('phone_number', models.CharField(blank=True, max_length=18, null=True, verbose_name='Foydalnuvchi Raqami')),
                ('language', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telegram tili')),
            ],
            options={
                'verbose_name': 'Foydalanuvchi',
                'verbose_name_plural': 'Foydalanuvchilar',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.TextField()),
                ('product_quantity', models.IntegerField()),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.order')),
            ],
            options={
                'verbose_name': 'Zakaz qilingan mahsulot',
                'verbose_name_plural': 'Zakaz qilingan mahsulotlar',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=150, unique=True, verbose_name='Mahsulot nomi')),
                ('product_price', models.FloatField(verbose_name='Mahsulot narxi')),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Mahsulot rasmi')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.category')),
            ],
            options={
                'verbose_name': 'Mahsulot',
                'verbose_name_plural': 'Mahsulotlar',
            },
        ),
    ]