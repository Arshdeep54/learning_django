from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.aggregates import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .models import Product, Collection, OrderItem, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from .filters import ProductFilter


# Create your views here.


# now ProductList and productDetails  have similar syntax or duplications so we will use View sets here
# if you want to only do readonly oerations then use ReadOnlyModelViewSet for get the whole list or one individual product or collection
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination
    search_fields = ["title", "description"]
    ordering_fields = ["price", "last_update"]

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get("collection_id")
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset

    def get_serializer_context(self):
        return {"request": self.request}

    # we should change the delete fucntion with destroy as in ModelViewSet unlike RetrieveupdateDetroy..
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "this product cannot be deleted because it is asociated with orderitem"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     if product.orderitems.count() > 0:
    #         return Response(
    #             {
    #                 "error": "this product cannot be deleted because it is asociated with orderitem"
    #             },
    #             status=status.HTTP_405_METHOD_NOT_ALLOWED,
    #         )
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "this product cannot be deleted because it contains one or more products"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     collection = get_object_or_404(
    #         Collection.objects.annotate(products_count=Count("products")), pk=pk
    #     )
    #     if collection.products.count() > 0:
    #         return Response(
    #             {
    #                 "error": "this product cannot be deleted because it contains one or more products"
    #             },
    #             status=status.HTTP_405_METHOD_NOT_ALLOWED,
    #         )
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# class based generic views
# class ProductList(ListCreateAPIView):
#     # if there is no logic for setting the query set we can also make it simpler by initializing class variables
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     # otherwise we can use functions below
#     # def get_queryset(self):
#     #     return Product.objects.select_related("collection").all()
#     # def get_serializer_class(self):
#     #     return ProductSerializer
#     def get_serializer_context(self):
#         return {"request": self.request}


# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count("products")).all()
#     serializer_class = CollectionSerializer


# class ProductDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = "id"  # by default it is pk

#     # here delete method is custom we are overriding the original delete method which will just delete the data

#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count() > 0:
#             return Response(
#                 {
#                     "error": "this product cannot be deleted because it is asociated with orderitem"
#                 },
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             )
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class CollectionDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count("products")).all()
#     serializer_class = CollectionSerializer

#     def delete(self, request, pk):
#         collection = get_object_or_404(
#             Collection.objects.annotate(products_count=Count("products")), pk=pk
#         )
#         if collection.products.count() > 0:
#             return Response(
#                 {
#                     "error": "this product cannot be deleted because it contains one or more products"
#                 },
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             )
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class based views with APIView
# class ProductList(APIView):
#     def get(self, request):
#         query_set = Product.objects.select_related("collection").all()
#         serializer = ProductSerializer(
#             query_set, many=True, context={"request": request}
#         )
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # serializer.validated_data()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class CollectionList(APIView):
#     def get(self, request):
#         query_set = Collection.objects.annotate(products_count=Count("products")).all()
#         serializer = CollectionSerializer(
#             query_set, many=True, context={"request": request}
#         )
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # serializer.validated_data()
#         return Response(serializer.data, status=status.HTTP_201_CRECollection)


# class ProductDetails(APIView):
#     def get(self, reqquest, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)

#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count() > 0:
#             return Response(
#                 {
#                     "error": "this product cannot be deleted because it is asociated with orderitem"
#                 },
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             )
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class CollectionDetails(APIView):
#     def get(self, request, pk):
#         collection = get_object_or_404(
#             Collection.objects.annotate(products_count=Count("products")), pk=pk
#         )
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         collection = get_object_or_404(
#             Collection.objects.annotate(products_count=Count("products")), pk=pk
#         )
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, pk):
#         collection = get_object_or_404(
#             Collection.objects.annotate(products_count=Count("products")), pk=pk
#         )
#         if collection.products.count() > 0:
#             return Response(
#                 {
#                     "error": "this product cannot be deleted because it contains one or more products"
#                 },
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             )
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


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
