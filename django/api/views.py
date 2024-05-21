from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from my_app.models import User, Category, Product, Order, OrderItem
from .serializers import UserSerializer, ProductSerialzer, CategorySerializer, OrderSerializer, OrderitemSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    lookup_field = 'telegram_id'

    def get_queryset(self):
        telegram_id = self.kwargs['telegram_id']
        return User.objects.filter(telegram_id=telegram_id)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        category_id = self.kwargs['id']
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({'xatolik': "Categoriya toplmadi"}, status=status.HTTP_404_NOT_FOUND)

        products = Product.objects.filter(category=category)
        product_serializer = ProductSerialzer(products, many=True)

        category_serializer = self.get_serializer(category)
        response_data = {
            'category': category_serializer.data,
            'products': product_serializer.data
        }
        return Response(response_data)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerialzer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        product_id = self.kwargs['id']
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"Xatolik": "Product toplmadi"}, status=status.HTTP_404_NOT_FOUND)

        product_serializer = self.get_serializer(product)
        return Response(product_serializer.data)


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerialzer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderitemSerializer


class OrderItemRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderitemSerializer
