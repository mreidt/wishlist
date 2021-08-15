from core.models import Produto, WishlistItem
from rest_framework import serializers


class WishlistItemSerializer(serializers.ModelSerializer):
    """Serializer for WishlistItem object"""

    class Meta:
        model = WishlistItem
        fields = ('id', 'client', 'product',)
        read_only_fields = ('id',)


class ProdutoSerializer(serializers.ModelSerializer):
    """Serializer for Produto object"""

    class Meta:
        model = Produto
        fields = ('id', 'price', 'image', 'brand', 'title', 'review_score',)
