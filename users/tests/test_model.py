from django.forms import ValidationError
from django.test import TestCase

from users.models import User


class AccountTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "username": "rex",
            "password": "abc123",
            "first_name": "tio",
            "last_name": "rex",
            "is_seller": False,
        }
        cls.user = User.objects.create_user(**cls.user_data)

    def test_user_fields(self):
        """Verifica se os campos foram preenchidos corretamente"""

        msg_username = "Verifique se os valores do campo `username` estão corretos"
        msg_first_name = "Verifique se os valores do campo `first_name` estão corretos"
        msg_last_name = "Verifique se os valores do campo `last_name` estão corretos"
        msg_is_seller = "Verifique se os valores do campo `is_seller` estão corretos"

        self.assertEqual(self.user.username, self.user_data["username"], msg_username)
        self.assertEqual(
            self.user.first_name, self.user_data["first_name"], msg_first_name
        )
        self.assertEqual(
            self.user.last_name, self.user_data["last_name"], msg_last_name
        )
        self.assertEqual(
            self.user.is_seller, self.user_data["is_seller"], msg_is_seller
        )

    def test_unique_username(self):
        """Verifica se o `username` já existe"""

        newUser = {
            "username": "rex",
            "password": "abc123",
            "first_name": "giuseppe",
            "last_name": "cadura",
            "is_seller": False,
        }

        user = User(**newUser)
        msg = "username already exists."

        with self.assertRaisesMessage(ValidationError, msg):
            user.full_clean()
