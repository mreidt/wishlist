import requests
from core.models import Produto, WishlistItem
from rest_framework import (authentication, generics, permissions, status,
                            viewsets)
from rest_framework.response import Response
from wishlist.serializers import (ProdutoSerializer,
                                  WishlistItemDetailSerializer,
                                  WishlistItemSerializer)

EXT_URL = 'http://challenge-api.luizalabs.com/api/product'


class WishlistItemViewSet(viewsets.ModelViewSet, generics.DestroyAPIView):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(client=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return WishlistItemDetailSerializer

        return self.serializer_class

    def exist_product_database(self, product_id):
        """Verify if the product exists in database"""
        return Produto.objects.filter(id=product_id).exists()

    def exist_product_api(self, product_id):
        """Verify if the product exists in external API"""
        try:
            res = requests.get(f'{EXT_URL}/{product_id}/')
            if res.status_code == status.HTTP_200_OK:
                return res.json()
            else:
                return None
        except Exception:
            return None

    def get_product_from_db(self, product_id):
        """Get product from db"""
        return Produto.objects.get(id=product_id)

    def create_product(self, product):
        """Create product on DB"""
        if product.get('reviewScore', None):
            product['review_score'] = product.pop('reviewScore')
        serializer = ProdutoSerializer()
        return serializer.create(validated_data=product)

    def return_product(self, product_id):
        """Return Product object if exists"""
        if self.exist_product_database(product_id):
            return self.get_product_from_db(product_id)
        product = self.exist_product_api(product_id)
        if product:
            return self.create_product(product)
        return None

    def create(self, request, *args, **kwargs):
        if int(request.user.id) != int(request.data.get('client')):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        product = self.return_product(request.data.get('product'))
        if product:
            super().create(request, *args, **kwargs)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
