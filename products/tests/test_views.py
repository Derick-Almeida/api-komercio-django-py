import pdb
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status


from users.models import User
from products.models import Product

"""
        cls.admin_user_data = {
            "username": "amb",
            "password": "abcd",
            "first_name": "Ambrósio",
            "last_name": "Silva",
            "is_seller": False,
        }
"""


class AccountViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.product_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 15,
        }
        cls.seller_user_data = {
            "username": "ale",
            "password": "abcd",
            "first_name": "Alexandre",
            "last_name": "Alves",
            "is_seller": True,
        }
        cls.normal_user_data = {
            "username": "dino",
            "password": "abcd",
            "first_name": "Dionizio",
            "last_name": "Notório",
            "is_seller": False,
        }
        cls.expected_detail_keys = {
            "id",
            "description",
            "price",
            "quantity",
            "is_active",
            "seller",
        }

    def test_only_seller_can_create_product(self):
        """Usuário vendedor deve ser capaz de criar um novo produto"""

        User.objects.create_user(**self.seller_user_data)

        login_data = {
            "username": self.seller_user_data["username"],
            "password": self.seller_user_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.post("/api/products/", self.product_data)

        expected_status_code = status.HTTP_201_CREATED

        result_status_code = response.status_code
        result_keys = set(response.data.keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_keys = "As chaves recebidas no retorno esta diferente do esperado"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(self.expected_detail_keys, result_keys, msg_keys)

    def test_normal_use_cannot_create_the_product(self):
        """Usuário comum não deve ser capaz de criar um novo produto"""

        User.objects.create_user(**self.normal_user_data)

        login_data = {
            "username": self.normal_user_data["username"],
            "password": self.normal_user_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.post("/api/products/", self.product_data)

        expected_status_code = status.HTTP_403_FORBIDDEN
        expected_key = {"detail"}

        result_status_code = response.status_code
        result_key = set(response.data.keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_keys = "A chave recebida no retorno esta diferente do esperado"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(expected_key, result_key, msg_keys)

    def test_only_the_seller_of_the_product_can_update_it(self):
        """O vendedor dono do produto deve ser capaz de atualiza-lo"""

        user = User.objects.create_user(**self.seller_user_data)
        product = Product.objects.create(**{**self.product_data, "user": user})

        login_data = {
            "username": self.seller_user_data["username"],
            "password": self.seller_user_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.patch(
            f"/api/products/{product.id}/", {"description": "Smartband XYZ 1000000"}
        )

        expected_status_code = status.HTTP_200_OK

        result_status_code = response.status_code
        result_keys = set(response.data.keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_keys = "As chaves recebidas no retorno esta diferente do esperado"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(self.expected_detail_keys, result_keys, msg_keys)

    def test_anyone_can_list_products(self):
        """Qualquer um deve ser capaz de listar todos os produtos"""

        User.objects.create_user(**self.seller_user_data)

        login_data = {
            "username": self.seller_user_data["username"],
            "password": self.seller_user_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])
        self.client.post("/api/products/", self.product_data)

        response = self.client.get("/api/products/")

        expected_status_code = status.HTTP_200_OK
        expected_keys = {"count", "next", "previous", "results"}
        expected_results_obj_keys = {
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        }

        result_status_code = response.status_code
        result_keys = set(response.data.keys())
        result_results_obj_keys = set(response.data["results"][0].keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_keys = "As chaves recebidas no retorno esta diferente do esperado"
        msg_obj_keys = (
            "As chaves do produto na lista de resultados esta diferente do esperado"
        )

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(expected_keys, result_keys, msg_keys)
        self.assertSetEqual(
            expected_results_obj_keys, result_results_obj_keys, msg_obj_keys
        )

    def test_anyone_can_filter_products(self):
        """Qualquer um deve ser capaz de buscar um produto"""

        user = User.objects.create_user(**self.seller_user_data)
        product = Product.objects.create(**{**self.product_data, "user": user})

        response = self.client.get(f"/api/products/{product.id}/")

        expected_status_code = status.HTTP_200_OK

        result_status_code = response.status_code
        result_keys = set(response.data.keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_keys = "As chaves recebidas no retorno esta diferente do esperado"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(self.expected_detail_keys, result_keys, msg_keys)

    def test_wrong_keys(self):
        """Usuário vendedor deve ser capaz de criar um novo produto"""

        User.objects.create_user(**self.seller_user_data)

        login_data = {
            "username": self.seller_user_data["username"],
            "password": self.seller_user_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.post("/api/products/", {})

        expected_status_code = status.HTTP_400_BAD_REQUEST
        expected_Keys = {"description", "price", "quantity"}

        result_status_code = response.status_code
        result_keys = set(response.data.keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_keys = "As chaves recebidas no retorno esta diferente do esperado"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(expected_Keys, result_keys, msg_keys)

    def test_create_product_with_negative_quantity(self):
        """Não deve ser capaz de criar um novo produto com o valor de `quantity` negativo"""

        User.objects.create_user(**self.seller_user_data)

        login_data = {
            "username": self.seller_user_data["username"],
            "password": self.seller_user_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])
        product_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": -15,
        }

        response = self.client.post("/api/products/", product_data)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        expected_key = {"quantity"}

        result_status_code = response.status_code
        result_key = set(response.data.keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_key = "A chave recebida no retorno esta diferente do esperado"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(expected_key, result_key, msg_key)
