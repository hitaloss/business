from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from sqlite3 import IntegrityError
from django.test import TestCase
from users.models import User

from django.core.exceptions import ValidationError
from django.db import IntegrityError


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_data = {
            "username": "franks",
            "first_name": "Frank",
            "last_name": "Stein",
            "is_seller": True,
        }
        cls.user = User.objects.create_user(**user_data)

    def test_if_username_can_be_unique(self):
        user_data = {
            "username": "franks",
            "first_name": "While",
            "last_name": "Crocodile",
            "is_seller": True,
        }

        with self.assertRaises(IntegrityError):
            User.objects.create_user(**user_data)

    def test_first_name_max_length(self):
        expected_length = 50
        actual_length = User._meta.get_field("first_name").max_length
        msg = f"User first_name field must have up to {expected_length} characters"

        self.assertEqual(expected_length, actual_length, msg=msg)

    def test_first_name_max_length(self):
        expected_length = 50
        actual_length = User._meta.get_field("last_name").max_length
        msg = f"User last_name field must have up to {expected_length} characters"

        self.assertEqual(expected_length, actual_length, msg=msg)

    def test_if_is_seller_field_can_receive_not_expected_type(self):
        user_data = {
            "username": "eddie",
            "first_name": "Later",
            "last_name": "Alligattor",
            "is_seller": "tru",
        }

        with self.assertRaises(ValidationError):
            User.objects.create_user(**user_data)


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

    def test_if_client_can_create_product_without_token(self):
        response = self.client.post("/api/products/")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."}
        )

    def test_users_patch_invalid_id(self):
        response = self.client.post("/api/users/123/")

        self.assertEqual(response.status_code, 404)

    def test_wrong_keys_on_seller_creation(self):
        common_data = {
            "usename": "hudson",
            "firstName": "hud",
            "lastName": "son",
            "isSeller": True,
        }
        with self.assertRaises(TypeError):
            User.objects.create_user(**common_data)

    def test_wrong_keys_on_common_creation(self):
        common_data = {
            "usename": "hudson",
            "firstName": "hud",
            "lastName": "son",
            "isSeller": False,
        }
        with self.assertRaises(TypeError):
            User.objects.create_user(**common_data)

    def test_login_seller_return_token(self):
        token = Token.objects.create(user=self.seller)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"username": self.seller.username, "password": "1234"}
        response = self.client.post("/api/login/", data=data)

        self.assertEqual(response.data, {"token": token.key})

    def test_login_common_return_token(self):
        token = Token.objects.create(user=self.common)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"username": self.common.username, "password": "1234"}
        response = self.client.post("/api/login/", data=data)

        self.assertEqual(response.data, {"token": token.key})

    def test_update_account_not_being_owner(self):
        token = Token.objects.create(user=self.common)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"first_name": "feijoada"}
        response = self.client.patch(f"/api/accounts/{self.seller.id}/", data=data)

        self.assertEqual(response.status_code, 403)

    def test_trying_to_deactivate_account_not_being_administrator(self):
        token = Token.objects.create(user=self.common)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"is_active": False}
        response = self.client.patch(
            f"/api/accounts/{self.seller.id}/management/", data=data
        )

        self.assertEqual(response.status_code, 403)

    def test_trying_to_deactivate_account_being_the_administrator(self):
        token = Token.objects.create(user=self.superuser)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"is_active": False}
        response = self.client.patch(
            f"/api/accounts/{self.seller.id}/management/", data=data
        )

        self.assertEqual(response.status_code, 200)

    def test_trying_to_activate_account_not_being_the_administrator(self):
        token = Token.objects.create(user=self.common)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"is_active": True}
        response = self.client.patch(
            f"/api/accounts/{self.seller.id}/management/", data=data
        )

        self.assertEqual(response.status_code, 403)

    def test_anyone_can_list_all_users(self):
        token = Token.objects.create(user=self.common)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.get(f"/api/accounts/")

        self.assertEqual(response.status_code, 200)
