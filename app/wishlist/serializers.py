from core.models import Produto, WishlistItem
from rest_framework import serializers
from user.serializers import UserSerializer


class ProdutoSerializer(serializers.ModelSerializer):
    """Serializer for Produto object"""

    class Meta:
        model = Produto
        fields = ('id', 'price', 'image', 'brand', 'title', 'review_score',)


class WishlistItemSerializer(serializers.ModelSerializer):
    """Serializer for WishlistItem object"""
    class Meta:
        model = WishlistItem
        fields = ('id', 'client', 'product',)
        read_only_fields = ('id',)


class WishlistItemDetailSerializer(WishlistItemSerializer):
    """Serialize a wishlist item detail"""
    client = UserSerializer(read_only=True)
    product = ProdutoSerializer(read_only=True)
