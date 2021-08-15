from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user.serializers import UserSerializer

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')
REMOVE_URL = reverse('user:remove')
LIST_URL = reverse('user:list')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test_user@luizalabs.com',
            'password': 'testpass',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'test_user@luizalabs.com',
            'password': 'pass1234',
            'name': 'Test name',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 8 characters"""
        payload = {
            'email': 'test_user@luizalabs.com',
            'password': 'pw',
            'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test_user@luizalabs.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalide_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test_user@luizalabs.com', password='testpass')
        payload = {'email': 'test_user@luizalabs.com', 'password': 'wrong1234'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'test_user@luizalabs.com', 'password': 'wrong1234'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test_user@luizalabs.com',
            password='testpass',
            name='Test name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'new_name', 'password': 'newPass123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_remove_user_by_admin(self):
        """Test that an admin user can delete another user"""
        admin = get_user_model().objects.create_superuser(
            email='adminuser@luizalabs.com',
            password='admin1234'
        )
        another_user = create_user(
            email='commonuser@luizalabs.com',
            password='pass1234',
            name='common user'
        )

        client2 = APIClient()
        client2.force_authenticate(user=admin)

        res = client2.delete(REMOVE_URL, {'user_id': another_user.id})
        users = get_user_model().objects.all()

        self.assertNotIn(another_user, users)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_remove_user_no_admin_fails(self):
        """Test that a common user cannot remove another user"""
        another_user = create_user(
            email='commonuser@luizalabs.com',
            password='pass1234',
            name='common user'
        )

        res = self.client.delete(REMOVE_URL, {'user_id': another_user.id})
        users = get_user_model().objects.all()

        self.assertIn(another_user, users)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_remove_own_profile(self):
        """Test that an user can remove own profile"""
        res = self.client.delete(REMOVE_URL, {'user_id': self.user.id})
        users = get_user_model().objects.all()

        self.assertNotIn(self.user, users)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_remove_with_no_parameters(self):
        """Test that a delete with no parameters removes user"""
        res = self.client.delete(REMOVE_URL)
        users = get_user_model().objects.all()

        self.assertNotIn(self.user, users)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_not_allowed_to_remove_endpoint(self):
        """Test that GET is not allowed to remove endpoint"""
        res = self.client.get(REMOVE_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_not_allowed_to_remove_endpoint(self):
        """Test that POST is not allowed to remove endpoint"""
        res = self.client.post(REMOVE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_users(self):
        """Test retrieve users"""
        create_user(
            email='commonuser@luizalabs.com',
            password='pass1234',
            name='common user'
        )
        admin = get_user_model().objects.create_superuser(
            email='admin@luizalabs.com',
            password='adminpass123'
        )

        client2 = APIClient()
        client2.force_authenticate(user=admin)
        users = get_user_model().objects.all()
        serializer = UserSerializer(users, many=True)

        res = client2.get(LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retreive_users_no_admin_fails(self):
        """Test only admin users can list all users"""
        create_user(
            email='commonuser@luizalabs.com',
            password='pass1234',
            name='common user'
        )

        res = self.client.get(LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_not_allowed_to_list_endpoint(self):
        """Test post method not allowed on list endpoint"""
        admin = get_user_model().objects.create_superuser(
            email='admin@luizalabs.com',
            password='adminpass123'
        )

        client2 = APIClient()
        client2.force_authenticate(user=admin)
        res = client2.post(LIST_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_not_allowed_to_list_endpoint(self):
        """Test delete method not allowed on list endpoint"""
        admin = get_user_model().objects.create_superuser(
            email='admin@luizalabs.com',
            password='adminpass123'
        )

        client2 = APIClient()
        client2.force_authenticate(user=admin)
        res = client2.delete(LIST_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_not_allowed_to_list_endpoint(self):
        """Test patch method not allowed on list endpoint"""
        admin = get_user_model().objects.create_superuser(
            email='admin@luizalabs.com',
            password='adminpass123'
        )

        client2 = APIClient()
        client2.force_authenticate(user=admin)
        res = client2.patch(LIST_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_not_allowed_to_list_endpoint(self):
        """Test put method not allowed on list endpoint"""
        admin = get_user_model().objects.create_superuser(
            email='admin@luizalabs.com',
            password='adminpass123'
        )

        client2 = APIClient()
        client2.force_authenticate(user=admin)
        res = client2.put(LIST_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
