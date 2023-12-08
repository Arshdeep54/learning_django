from .models import Collection, Product
from rest_framework.serializers import Serializer
from rest_framework import serializers
from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "price",
            "inventory",
            "taxed_price",
            "collection",
        ]

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # priceToDisplay = serializers.DecimalField(
    #     max_digits=6, decimal_places=2, source="price"
    # )
    taxed_price = serializers.SerializerMethodField(method_name="taxcalculate")
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(), view_name="collection_detail"
    # )

    def taxcalculate(self, product):
        return product.price * Decimal(1.1)
