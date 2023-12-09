from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Product, Collection
from django.db.models.aggregates import Count
from .serializers import ProductSerializer, CollectionSerializer

# Create your views here.


class ProductList(APIView):
    def get(self, request):
        query_set = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(
            query_set, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # serializer.validated_data()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionList(APIView):
    def get(self, request):
        query_set = Collection.objects.annotate(products_count=Count("products")).all()
        serializer = CollectionSerializer(
            query_set, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # serializer.validated_data()
        return Response(serializer.data, status=status.HTTP_201_CRECollection)


class ProductDetails(APIView):
    def get(self, reqquest, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response(
                {
                    "error": "this product cannot be deleted because it is asociated with orderitem"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionDetails(APIView):
    def get(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count("products")), pk=pk
        )
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    def put(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count("products")), pk=pk
        )
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count("products")), pk=pk
        )
        if collection.products.count() > 0:
            return Response(
                {
                    "error": "this product cannot be deleted because it contains one or more products"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# function based views
# @api_view(["GET", "POST"])
# def product_list(request):
#     if request.method == "GET":
#         query_set = Product.objects.select_related("collection").all()
#         serializer = ProductSerializer(
#             query_set, many=True, context={"request": request}
#         )
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # serializer.validated_data()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["GET", "PUT", "DELETE"])
# def product_details(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == "GET":
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == "DELETE":
#         if product.orderitems.count() > 0:
#             return Response(
#                 {
#                     "error": "this product cannot be deleted because it is asociated with orderitem"
#                 },
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             )
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(["GET", "PUT", "DELETE"])
# def collection_details(request, pk):
#     collection = get_object_or_404(
#         Collection.objects.annotate(products_count=Count("products")), pk=pk
#     )
#     if request.method == "GET":
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == "DELETE":
#         if collection.products.count() > 0:
#             return Response(
#                 {
#                     "error": "this product cannot be deleted because it contains one or more products"
#                 },
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             )
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def collection_list(request):
    if request.method == "GET":
        query_set = Collection.objects.annotate(products_count=Count("products")).all()
        serializer = CollectionSerializer(query_set, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # serializer.validated_data()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
