from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestRegistrationView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            "first_name": "Test",
            "last_name": "User",
            "username": "TestUser",
            "password1": "testing12",
            "password2": "testing12",
        }
        self.url = reverse("create_user")

    def test_registration_POST(self):
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/login/")

    def test_registration_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()
        self.u = get_user_model().objects.create_user(
            username="TestUser", password="testing12"
        )
        self.url = reverse("login")

    def test_login_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_login_POST(self):
        # Test wrong creds
        response = self.client.post(
            self.url, {"username": "TestUser", "password": "testings"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("users/create.html")

        # Test correct creds
        response = self.client.post(
            self.url, {"username": "TestUser", "password": "testing12"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/")


class TestLogoutView(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.u = get_user_model().objects.create_user(
            username="TestUser", password="testing12"
        )
        self.client.login(username="TestUser", password="testing12")
        self.url = reverse("logout")

    def test_logout_POST(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/")


class TestUpdateView(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.u = get_user_model().objects.create_user(
            username="TestUser", password="testing12"
        )
        self.url = reverse("update_user", kwargs={"pk": self.u.pk})

    def test_update_GET(self):
        # Test without login
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/login/")

        # Test with login
        self.client.login(username="TestUser", password="testing12")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="TestUser", status_code=200)

    def test_update_POST(self) -> None:
        # Test wrong inputs
        self.client.login(username="TestUser", password="testing12")
        post_response = self.client.post(
            self.url,
            {
                "first_name": "Test",
                "last_name": "User",
                "username": "TestUser",
                "password2": "testing12",
            },
        )
        self.assertEqual(post_response.status_code, 302)
        self.assertEqual("", self.u.first_name)

        # Test correct inputs
        self.client.login(username="TestUser", password="testing12")
        post_response = self.client.post(
            self.url,
            {
                "first_name": "Test",
                "last_name": "User",
                "username": "TestUser",
                "password1": "testing12",
                "password2": "testing12",
            },
        )
        self.assertEqual(post_response.status_code, 302)
        updated_user = get_user_model().objects.get(username="TestUser")
        self.assertEqual("Test", updated_user.first_name)


class TestDeleteUserView(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.u = get_user_model().objects.create_user(
            username="TestUser", first_name="Test", password="testing12"
        )
        self.u2 = get_user_model().objects.create_user(
            username="TestUser2", first_name="Test", password="testing12"
        )
        self.url = reverse("delete_user", kwargs={"pk": self.u.pk})
        self.url2 = reverse("delete_user", kwargs={"pk": self.u2.pk})

    def test_delete_GET(self):
        # Test without login
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        # Test attempt to delete wrong user
        self.client.login(username="TestUser", password="testing12")
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 302)

        # Test with login
        self.client.login(username="TestUser", password="testing12")
        response = self.client.get(self.url)
        self.assertContains(response, self.u.first_name, status_code=200)

    def test_delete_POST(self):
        self.client.login(username="TestUser2", password="testing12")
        user_pk = self.u2.pk
        users_pk = get_user_model().objects.values_list("pk")
        response = self.client.post(self.url2)
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(user_pk, users_pk)


class TestUsersViews(TestCase):
    def test_main_index_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_users_index_view(self):
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)
