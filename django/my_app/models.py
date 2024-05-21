from django.db import models


class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel_files/', verbose_name="Excel Fayl")

    def __str__(self):
        return str(self.file)


class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True, null=True, verbose_name="Foydalanuvchi ID")
    username = models.CharField(max_length=50, null=True, verbose_name="Foydalanuvchi username")
    user_full_name = models.CharField(max_length=25, null=True, verbose_name="Foydalanuvchi Ismi Familyasi")
    phone_number = models.CharField(max_length=18, blank=True, null=True, verbose_name="Foydalnuvchi Raqami")
    language = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telegram tili")

    def __str__(self):
        return f"{self.user_full_name} {self.telegram_id}"

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"


class Category(models.Model):
    category_name = models.CharField(max_length=30, unique=True, verbose_name="Kategoriya nomi")

    def __str__(self):
        return f"{self.category_name}"

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


class Product(models.Model):
    product_name = models.CharField(max_length=150, unique=True, verbose_name="Mahsulot nomi")
    product_price = models.FloatField(verbose_name="Mahsulot narxi")
    product_image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Mahsulot rasmi")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product_name}"

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"


class Order(models.Model):
    customer_name = models.TextField()
    customer_phone = models.CharField(max_length=50)
    customer_user_name = models.CharField(max_length=120)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name}"

    class Meta:
        verbose_name = "Zakazchi"
        verbose_name_plural = "Zakazchilar"


class OrderItem(models.Model):
    product_name = models.TextField()
    product_quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product_name}"

    class Meta:
        verbose_name = "Zakaz qilingan mahsulot"
        verbose_name_plural = "Zakaz qilingan mahsulotlar"

