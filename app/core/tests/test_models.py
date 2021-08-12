
import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from core import models


class ModelTests(TestCase):

    # region User Tests
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'teste@luizalabs.com'
        password = 'pass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'teste@LUIZALABS.COM'
        user = get_user_model().objects.create_user(email, 'pass123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_innvalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'pass123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'teste@luizalabs.com',
            'pass123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_users_with_same_email_fails(self):
        """Test creating two users with same email raises error"""
        email = 'same_email@luizalabs.com'

        get_user_model().objects.create_user(email, 'pass123')

        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(email, '123pass')
    # endregion

    # region Cliente Testes
    def test_create_cliente(self):
        """Test creating a cliente"""
        cliente = models.Cliente.objects.create(
            name='Cliente Magalu',
            email='cliente_magalu@luizalabs.com'
        )

        self.assertEqual(str(cliente), cliente.email)

    def test_create_cliente_same_email_fails(self):
        """Test creating two clientes with same email fails"""
        email = 'cliente_magalu@luizalabs.com'

        models.Cliente.objects.create(name='Cliente 1', email=email)

        with self.assertRaises(IntegrityError):
            models.Cliente.objects.create(name='Cliente 2', email=email)
    # endregion

    # region Produto Testes
    def test_create_produto(self):
        """Test creating a produto"""
        produto_id = uuid.UUID('1bf0f365-fbdd-4e21-9786-da459d78dd1f')
        produto = models.Produto.objects.create(
            price=1699.0,
            image='http://challenge-api.luizalabs.com/' +
                  'images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg',
            brand='b\u00e9b\u00e9 confort',
            id=produto_id,
            title='Cadeira para Auto Iseos B\u00e9b\u00e9 Confort Earth Brown')

        self.assertEqual(str(produto), produto.title)
        search_produto = models.Produto.objects.get(id=produto_id)
        self.assertEqual(produto, search_produto)
    # endregion
