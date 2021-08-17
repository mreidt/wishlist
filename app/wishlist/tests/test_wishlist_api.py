import uuid

from core.models import Produto, WishlistItem
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from wishlist.serializers import WishlistItemSerializer

WISHLIST_URL = reverse('wishlist:wishlistitem-list')


def create_user(**params):
    """Create a user"""
    return get_user_model().objects.create_user(**params)


def sample_wishlist_item(**params):
    """Create a sample wishlist item"""
    return WishlistItem.objects.create(**params)


def sample_product(**params):
    """Create a sample product"""
    base_url = 'http://challenge-api.luizalabs.com/images'
    uid = uuid.UUID('9c0835e9-b53d-4a82-a483-f143c5459899')
    defaults = {
        'id': uid,
        'price': 10.9,
        'image': f'{base_url}/{uid}',
        'brand': 'sample brand',
        'title': 'Sample product'}
    defaults.update(params)

    return Produto.objects.create(**defaults)


def delete_url(wishlist_item_id):
    """Return delete wishlist item URL"""
    return reverse('wishlist:wishlistitem-detail', args=[wishlist_item_id])


class PublicWishlistApiTests(TestCase):
    """Test the Wishlist API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(WISHLIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWishlistApiTests(TestCase):
    """Test the Wishlist API (authenticated)"""

    def setUp(self):
        self.user = create_user(
            email='test_user@luizalabs.com',
            password='testpass',
            name='Test name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_wishlist(self):
        """Test creating a wishlist successful"""
        product_uuid = uuid.UUID('af04c0ee-7137-4848-fd33-a2d148412095')
        payload = {
            'client': self.user.id,
            'product': product_uuid
        }

        res = self.client.post(WISHLIST_URL, payload)
        wishlists = WishlistItem.objects.all()

        self.assertEqual(len(wishlists), 1)
        self.assertEqual(wishlists[0].product.id, product_uuid)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_wishlist_invalid_product_fails(self):
        """Test creating a wishlist with invalid product fails"""
        product_uuid = uuid.UUID('b815b43b-0e0d-4514-b503-29f1bdfd2db8')
        payload = {
            'client': self.user.id,
            'product': product_uuid
        }

        res = self.client.post(WISHLIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_wishlist_repeated_products_fails(self):
        """Test that a wishlist can not accept repeated products"""
        product_uuid = uuid.UUID('af04c0ee-7137-4848-fd33-a2d148412095')
        product = sample_product(id=product_uuid)
        sample_wishlist_item(client=self.user, product=product)
        payload = {
            'client': self.user.id,
            'product': product_uuid
        }

        res = self.client.post(WISHLIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_wishlist(self):
        """Retrieve authenticated user wishlits"""
        product_uuid = uuid.UUID('af04c0ee-7137-4848-fd33-a2d148412095')
        product = sample_product(id=product_uuid)
        sample_wishlist_item(client=self.user, product=product)

        wishlist_items = WishlistItem.objects.all()

        res = self.client.get(WISHLIST_URL)
        serializer = WishlistItemSerializer(wishlist_items, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_wishlist_item_another_user_fails(self):
        """Test creating a wishlist item for another user fails"""
        product_uuid = uuid.UUID('af04c0ee-7137-4848-fd33-a2d148412095')
        sample_product(id=product_uuid)

        user2 = create_user(
            email='newemail@luizalabs.com',
            password='testpass',
            name='anothe user'
        )
        payload = {
            'client': user2.id,
            'product': product_uuid
        }

        res = self.client.post(WISHLIST_URL, payload)
        wishlist_items = WishlistItem.objects.filter(client=user2)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(wishlist_items), 0)

    def test_retrieve_wishlist_authenticated_user_only(self):
        """Test the retrieve wishlist returns only authenticated user info"""
        product_uuid = uuid.UUID('af04c0ee-7137-4848-fd33-a2d148412095')
        product = sample_product(id=product_uuid)

        user2 = create_user(
            email='newuser@luizalabs.com',
            password='testpass',
            name='Test name'
        )
        sample_wishlist_item(client=self.user, product=product)
        sample_wishlist_item(client=user2, product=product)
        client2 = APIClient()
        client2.force_authenticate(user=user2)

        res = client2.get(WISHLIST_URL)
        wishlist_items = WishlistItem.objects.filter(client=user2)

        serializer = WishlistItemSerializer(wishlist_items, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_remove_product_from_wishlist(self):
        """Test user can remove products from wishlist"""
        product_uuid = uuid.UUID('af04c0ee-7137-4848-fd33-a2d148412095')
        product = sample_product(id=product_uuid)

        wishlist_item = sample_wishlist_item(client=self.user, product=product)

        url = delete_url(wishlist_item_id=wishlist_item.id)
        res = self.client.delete(url)
        wishlist_items = WishlistItem.objects.all()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(wishlist_items), 0)

    def test_remove_product_from_another_user_wishlist_fails(self):
        """Test user can remove products from another user wishlist fails"""
        product_uuid = uuid.UUID('af04c0ee-7137-4848-fd33-a2d148412095')
        product = sample_product(id=product_uuid)

        wishlist_item = sample_wishlist_item(client=self.user, product=product)
        user2 = create_user(
            email='newuser@luizalabs.com',
            password='testpass',
            name='Test name'
        )
        client2 = APIClient()
        client2.force_authenticate(user=user2)

        url = delete_url(wishlist_item_id=wishlist_item.id)
        res = client2.delete(url)
        wishlist_items = WishlistItem.objects.filter(id=wishlist_item.id)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(wishlist_item, wishlist_items)
