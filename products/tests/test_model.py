from django.test import TestCase

from products.models import Product
from users.models import User


class AccountTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.product_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 15,
        }
        cls.user_data = {
            "username": "rex",
            "password": "abc123",
            "first_name": "tio",
            "last_name": "rex",
            "is_seller": False,
        }
        cls.user = User.objects.create_user(**cls.user_data)
        cls.product = Product.objects.create(**{**cls.product_data, "user": cls.user})

    def test_user_fields(self):
        """Verifica se os campos foram preenchidos corretamente"""

        msg_description = (
            "Verifique se os valores do campo `description` estão corretos"
        )
        msg_price = "Verifique se os valores do campo `price` estão corretos"
        msg_quantity = "Verifique se os valores do campo `quantity` estão corretos"

        self.assertEqual(
            self.product.description, self.product_data["description"], msg_description
        )
        self.assertEqual(self.product.price, self.product_data["price"], msg_price)
        self.assertEqual(
            self.product.quantity, self.product_data["quantity"], msg_quantity
        )

    def test_product_contain_unique_user(self):
        """Verificando se o `product` possui apenas um `user`"""

        self.assertIs(self.product.user, self.user)
