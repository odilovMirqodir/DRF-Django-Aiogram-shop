from rest_framework import serializers
from my_app.models import User, Category, Product, Order, OrderItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerialzer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_product_image(self, obj):
        if obj.product_image:
            base_url = "http://127.0.0.1:8000"
            return f"{base_url}{obj.product_image.url}"
        return None


class OrderitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderitemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
