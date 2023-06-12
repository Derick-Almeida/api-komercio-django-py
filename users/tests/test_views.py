from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status

from users.models import User


class AccountViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
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
        cls.expected_keys = {
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        }
        cls.admin_user_data = {
            "username": "amb",
            "password": "abcd",
            "first_name": "Ambrósio",
            "last_name": "Silva",
            "is_seller": False,
        }
        cls.update_data = {
            "first_name": "Roberto",
            "last_name": "Carlos",
        }

        cls.admin_user = User.objects.create_superuser(**cls.admin_user_data)
        token = Token.objects.create(user=cls.admin_user)
        cls.admin_token = token.key

    def test_create_user_seller(self):
        """Deve ser capaz de criar um novo usuário vendedor"""

        response = self.client.post("/api/accounts/", self.seller_user_data)

        expected_status_code = status.HTTP_201_CREATED

        result_status_code = response.status_code
        result_keys = set(response.data.keys())
        result_is_seller = response.data["is_seller"]

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_keys = "As chaves recebidas no retorno esta diferente do esperado"
        msg_is_seller = (
            "Is_seller deve ser igual a `true` para o usuário ser um vendedor"
        )

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(self.expected_keys, result_keys, msg_keys)
        self.assertTrue(result_is_seller, msg_is_seller)

    def test_create_user_normal(self):
        """Deve ser capaz de criar um novo usuário comum"""

        response = self.client.post("/api/accounts/", self.normal_user_data)

        expected_status_code = status.HTTP_201_CREATED

        result_status_code = response.status_code
        result_keys = set(response.data.keys())
        result_is_seller = response.data["is_seller"]

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_keys = "As chaves recebidas no retorno esta diferente do esperado"
        msg_is_seller = "Is_seller deve ser igual a `false` para ser um usuário comum"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(self.expected_keys, result_keys, msg_keys)
        self.assertFalse(result_is_seller, msg_is_seller)

    def test_create_user_invalid_keys(self):
        """Não deve ser capaz de criar um novo usuário caso os dados passados estejam errados"""

        response = self.client.post("/api/accounts/", {})

        expected_status_code = status.HTTP_400_BAD_REQUEST
        expected_keys = {"username", "password", "first_name", "last_name"}

        result_status_code = response.status_code
        result_keys = set(response.data.keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_keys = "As chaves recebidas no retorno esta diferente do esperado"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(expected_keys, result_keys, msg_keys)

    def test_create_user_with_already_existing_username(self):
        """Não deve ser capaz de criar um novo usuário caso o `username` passado ja esteja em uso"""

        self.client.post("/api/accounts/", self.seller_user_data)

        response = self.client.post("/api/accounts/", self.seller_user_data)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code
        msg_status_code = "O status code recebido esta diferente do esperado"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)

    def test_return_of_seller_user_token(self):
        """Deve ser capaz efetuar o login de um usuário vendedor"""

        User.objects.create_user(**self.seller_user_data)

        login_data = {
            "username": self.seller_user_data["username"],
            "password": self.seller_user_data["password"],
        }

        response = self.client.post("/api/login/", login_data)

        expected_status_code = status.HTTP_200_OK
        expected_key = {"token"}

        result_status_code = response.status_code
        result_key = set(response.data.keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_key = "A chave recebida no retorno deve se chamar token"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(expected_key, result_key, msg_key)

    def test_return_of_normal_user_token(self):
        """Deve ser capaz efetuar o login de um usuário comum"""

        User.objects.create_user(**self.normal_user_data)

        login_data = {
            "username": self.normal_user_data["username"],
            "password": self.normal_user_data["password"],
        }

        response = self.client.post("/api/login/", login_data)

        expected_status_code = status.HTTP_200_OK
        expected_key = {"token"}

        result_status_code = response.status_code
        result_key = set(response.data.keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_key = "A chave recebida no retorno deve se chamar token"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(expected_key, result_key, msg_key)

    def test_invalid_seller_user_login(self):
        """Usuário vendedor não deve ser capaz de efetuar o login com dados inválidos"""

        User.objects.create_user(**self.seller_user_data)

        login_data = {
            "username": self.seller_user_data["username"],
            "password": "banana",
        }

        response = self.client.post("/api/login/", login_data)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        expected_key = {"non_field_errors"}

        result_status_code = response.status_code
        result_key = set(response.data.keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_key = "A chave recebida no retorno deve se chamar token"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(expected_key, result_key, msg_key)

    def test_invalid_normal_user_login(self):
        """Usuário vendedor não deve ser capaz de efetuar o login com dados inválidos"""

        User.objects.create_user(**self.normal_user_data)

        login_data = {
            "username": self.normal_user_data["username"],
            "password": "banana",
        }

        response = self.client.post("/api/login/", login_data)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        expected_key = {"non_field_errors"}

        result_status_code = response.status_code
        result_key = set(response.data.keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_key = "A chave recebida no retorno deve se chamar token"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(expected_key, result_key, msg_key)

    def test_only_account_owner_can_update_data(self):
        """O dono da conta deve ser capaz de atualizar seus dados"""

        user = User.objects.create_user(**self.normal_user_data)

        login_data = {
            "username": self.normal_user_data["username"],
            "password": self.normal_user_data["password"],
        }

        login = self.client.post("/api/login/", login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])

        response = self.client.patch(f"/api/accounts/{user.id}/", self.update_data)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code
        result_keys = set(response.data.keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_keys = "As chaves recebidas no retorno esta diferente do esperado"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(self.expected_keys, result_keys, msg_keys)
        self.assertEqual(response.data["first_name"], self.update_data["first_name"])
        self.assertEqual(response.data["last_name"], self.update_data["last_name"])

    def test_only_admin_can_disable_it(self):
        """Usuário admin deve ser capaz de desativar a conta de outro usuário"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token)
        user = self.client.post("/api/accounts/", self.seller_user_data)

        response = self.client.patch(
            f'/api/accounts/{user.data["id"]}/management/', {"is_active": False}
        )

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code
        result_keys = set(response.data.keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_keys = "As chaves recebidas no retorno esta diferente do esperado"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(self.expected_keys, result_keys, msg_keys)
        self.assertFalse(response.data["is_active"])

    def test_only_admin_can_reactivate_accounts(self):
        """Usuário admin deve ser capaz de reativar a conta de outro usuário"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token)
        user = self.client.post("/api/accounts/", self.seller_user_data)

        response = self.client.patch(
            f'/api/accounts/{user.data["id"]}/management/', {"is_active": True}
        )

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code
        result_keys = set(response.data.keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_keys = "As chaves recebidas no retorno esta diferente do esperado"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(self.expected_keys, result_keys, msg_keys)
        self.assertTrue(response.data["is_active"])

    def test_anyone_can_list_users(self):
        """Deve ser capaz de listar usuários"""

        self.client.post("/api/accounts/", self.seller_user_data)

        response = self.client.get("/api/accounts/")

        expected_status_code = status.HTTP_200_OK
        expected_keys = {"count", "next", "previous", "results"}
        expected_results_objects_keys = self.expected_keys

        result_status_code = response.status_code
        result_keys = set(response.data.keys())
        result_results_objects_keys = set(response.data["results"][0].keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_keys = "As chaves recebidas no retorno esta diferente do esperado"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(expected_keys, result_keys, msg_keys)
        self.assertSetEqual(
            expected_results_objects_keys, result_results_objects_keys, msg_keys
        )

    def test_anyone_can_list_users_by_dates(self):
        """Deve ser capaz de listar usuários por data"""

        self.client.post("/api/accounts/", self.seller_user_data)

        response = self.client.get("/api/accounts/newest/2")

        expected_status_code = status.HTTP_200_OK
        expected_keys = {"count", "next", "previous", "results"}
        expected_results_objects_keys = self.expected_keys

        result_status_code = response.status_code
        result_keys = set(response.data.keys())
        result_results_objects_keys = set(response.data["results"][0].keys())

        msg_status_code = "O status code recebido esta diferente do esperado"
        msg_keys = "As chaves recebidas no retorno esta diferente do esperado"

        self.assertEqual(expected_status_code, result_status_code, msg_status_code)
        self.assertSetEqual(expected_keys, result_keys, msg_keys)
        self.assertSetEqual(
            expected_results_objects_keys, result_results_objects_keys, msg_keys
        )
