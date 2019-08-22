from django.urls import path
from django.conf.urls import url
from .views import BooksList, indexView, OutOfStockBooksList, UserCreateAPIView, UserLoginAPIView, CategoryListAPIView, BookDetail


app_name = 'inventory'
urlpatterns = [
    path('', indexView, name="index"),
    path('inventory', BooksList.as_view(), name='inventory-list'),
    path('fetch-out-of-stock-books', OutOfStockBooksList.as_view(), name='out-of-stock-books'),
    path('register', UserCreateAPIView.as_view(), name = 'register'),
    path('login', UserLoginAPIView.as_view(), name = 'login'),
    path('category-list', CategoryListAPIView.as_view(), name = 'category-list'),
    path('inventory/<int:pk>', BookDetail.as_view(), name = 'book-detail'),
]