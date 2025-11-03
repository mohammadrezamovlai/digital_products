from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from .models import Product,File,Category
from.serialiizers import CategorySerializer,FileSerializer,ProductSerializer




class ProductListView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryListView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FileListView(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    def perform_create(self, serializer):
        product_id = self.kwargs['product_id']
        serializer.save(product_id=product_id)



# class ProductListView(APIView):
#     def get(self,request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products,many=True,context={'request':request})
#         return Response(serializer.data)

# class ProductDetailView(APIView):
#     def get(self,request,pk):
#         try:
#             product = Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             return Response('not found')
#         serializer = ProductSerializer(product,context={'request':request})
#         return Response(serializer.data)

