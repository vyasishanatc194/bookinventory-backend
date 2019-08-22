# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import BooksInventory, Category
import os
from django.conf import settings
from .serializers import GetBooksInventorySerializer, BooksInventorySerializer, UserCreateSerializer, UserLoginSerializer, CategorySerializer
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

def indexView(self):
    return HttpResponse('<h1>Welcome to Book Inventory Management')

def modify_input_for_multiple_files(instance, imagePath):
    data = {}
    data['book'] = instance
    data['image'] = imagePath
    return data

class BooksList(APIView):
    """
    List all Books.
    """
    permission_classes = (IsAuthenticated,) 
    def get(self, request, format=None):
        books = BooksInventory.objects.all()
        serializer = GetBooksInventorySerializer(books, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        print (request.data)
        addData = {}
        addData['title'] = request.data['title']
        addData['author'] = request.data['author']
        addData['isbn'] = request.data['isbn']
        addData['publisher'] = request.data['publisher']
        addData['publish_date'] = request.data['publish_date']
        addData['category'] = request.data['category']
        addData['no_of_stock'] = request.data['no_of_stock']
        print(type(request.data['image']))
        if type(request.data['image']) != str:
            addData['image'] = request.data['image']
        serializer = BooksInventorySerializer(data=addData)
        if serializer.is_valid():
            book = serializer.save()
            books = BooksInventory.objects.get(id=book.id)
            serializer = GetBooksInventorySerializer(books, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None):
        try:
            print (request.data)
            book = BooksInventory.objects.get(id=request.data['id'])
            # media_root = getattr(settings, 'MEDIA_ROOT', None)
            # print(media_root)
            # if media_root is not None:
            #     os.remove(os.path.join(media_root +'/', str(book.image)))
            book.delete()
            return Response({"message": "Deleted successfully!!"}, status=status.HTTP_204_NO_CONTENT)
        except BooksInventory.DoesNotExist:
            raise Http404

    def put(self, request,format=None):
        editData = {}
        try:
            book = BooksInventory.objects.get(id=request.data['id'])
            editData['id'] = request.data['id']
            editData['title'] = request.data['title']
            editData['author'] = request.data['author']
            editData['isbn'] = request.data['isbn']
            editData['publisher'] = request.data['publisher']
            editData['publish_date'] = request.data['publish_date']
            editData['category'] = request.data['category']
            editData['no_of_stock'] = request.data['no_of_stock']
            if type(request.data['image']) != str:
                editData['image'] = request.data['image']
            serializer = BooksInventorySerializer(book, data=editData)
            if book is not None:
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        except BooksInventory.DoesNotExist:
            raise Http404
class OutOfStockBooksList(APIView):
    """
    List all Books Which is Out of Stock.
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        books = BooksInventory.objects.filter(no_of_stock__lte=0)
        serializer = GetBooksInventorySerializer(books, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

#login and register views

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset= User.objects.all()

class UserLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data= request.data
        serializer = UserLoginSerializer(data= data)
        if serializer.is_valid(raise_exception = True):
            new_data = serializer.data
            return Response(new_data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class CategoryListAPIView(APIView):
    """
    List all Categories.
    """
    permission_classes = (IsAuthenticated,) 
    def get(self, request, format=None):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True,)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BookDetail(APIView):
    """
    Retrieve instance.
    """
    permission_classes = (IsAuthenticated,) 
    def get_object(self, pk):
        try:
            return BooksInventory.objects.get(pk=pk)
        except BooksInventory.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = GetBooksInventorySerializer(book, context={"request": request})
        return Response(serializer.data)