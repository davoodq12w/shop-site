from .serializers import *
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class ProductListApi(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    PageNumberPagination.page_size = 4


class ProductDetailsApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

