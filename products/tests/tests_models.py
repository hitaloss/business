from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from django.test import TestCase
from products.models import Product
from users.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError


class ProductsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        product_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 15,
        }
        user_data = {
            "username": "franks",
            "first_name": "While",
            "last_name": "Crocodile",
            "is_seller": True,
        }
        cls.user = User.objects.create_user(**user_data)
        cls.product = Product.objects.create(**product_data, user=cls.user)

    def test_if_description_field_can_be_null(self):
        product_data = {
            "description": None,
            "price": 100.99,
            "quantity": 15,
        }
        with self.assertRaises(IntegrityError):
            Product.objects.create(**product_data, user=self.user)

    def test_invalid_price_float_number(self):
        product_data = {
            "description": "Smartband XYZ 3.0",
            "price": "Bird flies away",
            "quantity": 15,
        }
        with self.assertRaises(ValidationError):
            Product.objects.create(**product_data, user=self.user)

    def test_if_quantity_can_be_a_negative_number(self):
        product_data = {
            "description": "Smartband XYZ 3.0",
            "price": "Bird flies away",
            "quantity": 150000012123.2131212,
        }
        with self.assertRaises(ValidationError):
            Product.objects.create(**product_data, user=self.user)

    def test_invalid_type_on_is_active_field(self):
        product_data = {
            "description": "Smartband XYZ 3.0",
            "price": "Bird flies away",
            "quantity": 150000012123.2131212,
        }
        with self.assertRaises(ValidationError):
            Product.objects.create(**product_data, user=self.user)

    def test_relation_with_user_table(self):
        expected_id = self.user.id
        actual_id = self.product.user_id
        msg = f"Id number {actual_id} must be equal to {expected_id}"

        self.assertEqual(expected_id, actual_id, msg=msg)


class TokenTest(APITestCase):
    def setUp(self):
        superuser_data = {
            "username": "scarecrow",
            "password": "1234",
            "first_name": "scare",
            "last_name": "crow",
            "is_seller": True,
        }
        self.superuser = User.objects.create_superuser(**superuser_data)

        seller_data = {
            "username": "batman",
            "password": "1234",
            "first_name": "bat",
            "last_name": "man",
            "is_seller": True,
        }
        self.seller = User.objects.create_user(**seller_data)

        common_data = {
            "username": "robin",
            "password": "1234",
            "first_name": "rob",
            "last_name": "son",
            "is_seller": False,
        }
        self.common = User.objects.create_user(**common_data)
        product_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 15,
        }

        self.product = Product.objects.create(**product_data, user_id=self.seller.id)

    def test_if_any_user_not_being_seller_can_create_a_product(self):
        token = Token.objects.create(user=self.common)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"description": "Smartband XYZ 3.0", "price": 100.99, "quantity": 15}
        response = self.client.post("/api/products/", data=data)

        self.assertEqual(response.status_code, 403)

    def test_if_anyone_can_modify_other_seller_products(self):
        token = Token.objects.create(user=self.common)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"price": 100.99}
        response = self.client.patch(f"/api/products/{self.product.id}/", data=data)

        self.assertEqual(response.status_code, 403)

    def test_if_anyone_can_list_all_product(self):
        token = Token.objects.create(user=self.common)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.get(f"/api/products/")

        self.assertEqual(response.status_code, 200)

    def test_if_it_is_possible_to_retrieve_only_one_product(self):
        token = Token.objects.create(user=self.seller)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.get(f"/api/products/{self.product.id}/")

        self.assertEqual(response.data["id"], str(self.product.id))

    def test_wrong_keys_on_product_creation(self):
        token = Token.objects.create(user=self.seller)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"descritio": "Smartband XYZ 3.0", "pricy": 100.99, "quantities": 15}
        response = self.client.post("/api/products/", data=data)

        self.assertEqual(response.status_code, 400)
