from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListCreateView.as_view(), name="user-list-create"),
    path('users/<int:telegram_id>/', views.UserDetailView.as_view(), name="user-detail"),

    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:id>/', views.CategoryDetailView.as_view(), name='categeory-detail'),

    path('products/', views.ProductListCreateView.as_view(), name='products-list-create'),
    path('products/<int:id>/', views.ProductDetailView.as_view(), name='products-detail'),

    path('orders/', views.OrderListCreateView.as_view(), name='orders-list-create'),
    path('orders/<int:pk>/', views.OrderRetriveUpdateDestroyView.as_view(), name='orders-detail'),

    path('order-items/', views.OrderItemListCreateView.as_view(), name='order-item-create-list'),
    path('order-items/<int:pk>/', views.OrderItemRetriveUpdateDestroyView.as_view(), name='order-item-detail'),
]
