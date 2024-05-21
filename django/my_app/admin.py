from django.contrib import admin
from django.utils.html import format_html
from my_app.models import User, Category, Product, Order, OrderItem, ExcelFile
from django.http import HttpResponse
import pandas as pd


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_full_name', 'telegram_id', 'username', 'phone_number', 'language']
    search_fields = ['user_full_name', 'telegram_id']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']
    search_fields = ['category_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_price', 'category', 'display_image']
    search_fields = ['product_name']
    list_display_links = ['product_price']
    list_editable = ['category']

    def display_image(self, obj):
        if obj.product_image:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px;" />'.format(obj.product_image.url)
            )
        else:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px;" />'.format(
                    'https://st3.depositphotos.com/23594922/31822/v/450/depositphotos_318221368-stock-illustration-missing-picture-page-for-website.jpg')
            )

    display_image.short_description = "Mahsulot rasmi"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'date']
    search_fields = ['customer_name']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_quantity', 'product_price', 'product_total_price', 'order']
    search_fields = ['order']


@admin.register(ExcelFile)
class ExcelFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'file']
    actions = ['filter_and_add_products']

    def filter_and_add_products(self, request, queryset):
        try:
            # Tanlangan faylni o'qib olish
            for excel_file in queryset:
                file_path = excel_file.file.path  # Faylni joylashgan joyini olish

                try:
                    df = pd.read_excel(file_path)  # Excel faylni malumotlarini o'qish

                    # Unikal kategoriyani olish
                    unique_categories = df['product'].str.split().str[0].unique()
                    created_categories_count = 0

                    for category_name in unique_categories:
                        if created_categories_count >= 15:
                            break
                        """Kategoriyani olish yoki yangi kategoriya yaratish"""
                        category, created = Category.objects.get_or_create(category_name=category_name)
                        if created:
                            created_categories_count += 1
                            # Kategoriyaga mos mahsulotlarni qoshish
                            filtered_products = df[df['product'].str.startswith(category_name)]

                            for index, row in filtered_products.iterrows():
                                product_name = row['product']  # Mahsulot nomi
                                product_price = row['price']
                                # Mahsulot narxini tekshirish
                                if pd.notna(product_price) and isinstance(product_price, (int, float)):
                                    product_price = float(product_price)
                                else:
                                    product_price = 0.0

                                # Agar mahsulot mavjud bo'lsa narxini va kategoriyasini yangilaymiz
                                existing_product = Product.objects.filter(product_name=product_name).first()
                                if existing_product:
                                    existing_product.product_price = product_price
                                    existing_product.category = category
                                    existing_product.save()
                                else:
                                    Product.objects.create(
                                        product_name=product_name,
                                        product_price=product_price,
                                        category=category
                                    )
                    # Productlar qoshilgandan keyin foydalanuvchiga chiqadigan soz
                    self.message_user(request, f"Mahsulotlar filter boldi")

                except Exception as e:
                    self.message_user(request, f"Faylni qoshishda xatolik {excel_file.id}:{str(e)}")

        except Exception as e:
            self.message_user(request, f"Error")

    filter_and_add_products.short_description = "Categorylarni filter qilish"


# admin.site.register(ExcelFile, ExcelFileAdmin)
