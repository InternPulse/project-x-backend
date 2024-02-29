from django.test import TestCase
from django.db.models.signals import post_save
from django.urls import reverse
from notifications.signals import send_welcome_email
from rest_framework.test import APIClient, APITestCase
from utils.types import test_response_schema
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from urllib.parse import urlencode
import random
import string
from .models import Profile, Questionnaire
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
User = get_user_model()
post_save.disconnect(send_welcome_email, sender=User)

def generate_random_username(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_url_with_parameters(viewname, kwargs=None, args=None, params=None):
    url = reverse(viewname, kwargs=kwargs, args=args)
    if params:
        url += '?' + urlencode(params)
    return url

class SignUpTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_with_wrong_values(self):
        data = {
            "email": "test@gmail.com",
            "password": "password",
            "first_name": "test",
            "last_name": "user",
        }
        url = reverse('signup')
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertTrue(len(data["errors"]) > 0)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(len(data["errors"]), 1)
        self.assertTrue(test_response_schema(data))

    def test_create_user_with_right_values(self):
        data = {
            "email": "test@gmail.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        }
        url = reverse('signup')
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["status"], 201)
        self.assertEqual(data["success"], True)
        self.assertTrue(test_response_schema(data))
    

class LoginTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        existing_user = User.objects.create_user(
            email="test@gmail.com",
            password="password123",
            first_name="Test",
            last_name="user",
            username=generate_random_username()
        )


    def test_login_with_invalid_password(self):
        data = {
            "email": "test@gmail.com",
            "password": "invalidpassword",
        }
        url = reverse('login')
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertTrue(len(data["errors"]) > 0)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(len(data["errors"]), 1)
        self.assertTrue(test_response_schema(data))

    def test_login_with_invalid_email(self):
        data = {
            "email": "invalidemail",
            "password": "password123",
        }
        url = reverse('login')
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertTrue(len(data["errors"]) > 0)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(len(data["errors"]), 1)
        self.assertTrue(test_response_schema(data))

    def test_login_with_invalid_email_and_password(self):
        data = {
            "email": "invalidemail@gmail.com",
            "password": "invalidpassword",
        }
        url = reverse('login')
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertTrue(len(data["errors"]) > 0)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(len(data["errors"]), 1)
        self.assertTrue(test_response_schema(data))

    def test_login_with_valid_email_non_existing_user(self):
        data = {
            "email": "test2@gmail.com",
            "password": "password123",
        }
        url = reverse('login')
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertTrue(len(data["errors"]) > 0)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(len(data["errors"]), 1)
        self.assertTrue(test_response_schema(data))

    def test_login_with_valid_email_existing_user(self):
        data = {
            "email": "test@gmail.com",
            "password": "password123",
        }
        url = reverse('login')
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(test_response_schema(data))


class UserManagementTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="password123",
            first_name="Test",
            last_name="User",
            username=generate_random_username()
        )
        self.user2 = User.objects.create_user(
            email="test2@gmail.com",
            password="password123",
            first_name="Test",
            last_name="User",
            username=generate_random_username()
        )

    def auth(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {str(refresh.access_token)}')

    def test_patch_update_with_authenticated_user(self):
        self.auth(self.user)
        data = {
            "first_name": "Updated",
            "last_name": "User",
        }
        url = reverse('user-detail', kwargs={'id': self.user.id})
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(data["success"], True)
        self.assertTrue(test_response_schema(data))

    def test_patch_update_without_authentication(self):
        data = {
            "first_name": "Updated",
            "last_name": "User",
        }
        url = reverse('user-detail', kwargs={'id': self.user.id})
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["status"], 401)
        self.assertEqual(data["success"], False)
        self.assertTrue(test_response_schema(data))

    def test_patch_update_with_invalid_data(self):
        self.auth(self.user)
        data = {
            "email": "test2@gmail.com",
            "last_name": "User",
        }
        url = reverse('user-detail', kwargs={'id': self.user.id})
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["success"], False)
        self.assertTrue(test_response_schema(data))
    
    def test_patch_unauthorized(self):
        data = {
            "role": "admin"
        }
        self.auth(self.user)
        url = reverse('user-detail', kwargs={'id': self.user.id})
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertTrue(test_response_schema(data))

    def test_get_user_existing(self):
        self.auth(self.user)
        url = reverse('user-detail', kwargs={'id': self.user.id})
        response = self.client.get(url)
        data = response.json()
        self.assertTrue(test_response_schema(data))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"]["email"], self.user.email)
    
    def test_get_user_not_existing(self):
        self.auth(self.user)
        url = reverse('user-detail', kwargs={'id': 234565687})
        response = self.client.get(url)
        data = response.json()
        self.assertTrue(test_response_schema(data))
        self.assertEqual(response.status_code, 404)

    def test_delete_with_authenticated_user(self):
        self.user.role = "admin"
        self.user.save()
        self.auth(self.user)
        url = reverse('user-detail', kwargs={'id': self.user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


    def test_delete_without_authentication(self):
        url = reverse('user-detail', kwargs={'id': self.user.id})
        response = self.client.delete(url)
        data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["status"], 401)
        self.assertEqual(data["success"], False)
        self.assertTrue(test_response_schema(data))
    
    def test_delete_without_permissions(self):
        self.user.role = "intern"
        self.user.save()
        self.auth(self.user)
        url = reverse('user-detail', kwargs={'id': self.user.id})
        response = self.client.delete(url)
        data = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertTrue(test_response_schema(data))
    
    def test_deactivate_user(self):
        self.user.role = "admin"
        self.user.save() 
        self.auth(self.user)
        url = get_url_with_parameters('user-detail', kwargs={'id': self.user2.id}, params={'deactivate': 'true'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.user2.refresh_from_db()
        self.assertFalse(self.user2.is_active)


class ProfileManageTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="password123",
            first_name="Test",
            last_name="User",
            username=generate_random_username()
        )
        self.user2 = User.objects.create_user(
            email="test2@gmail.com",
            password="password123",
            first_name="Test",
            last_name="User",
            username=generate_random_username()
        )
        profile = Profile.objects.create(user=self.user, address="2b centenary Garden PH")

    def auth(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {str(refresh.access_token)}')

    def test_get_profile(self):
        self.auth(self.user)
        url = reverse('profile')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(test_response_schema(data))

    def test_get_profile_not_existing(self):
        self.auth(self.user2)
        url = reverse('profile')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["status"], 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(test_response_schema(data))

    def test_get_profile_not_authenticated(self):
        url = reverse('profile')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["status"], 401)
        self.assertEqual(data["success"], False)
        self.assertTrue(test_response_schema(data))

    def test_create_profile_with_invalid_data(self):
        self.auth(self.user2)
        data = {
            "can_share_PI": "value1",
            "address": 50,
        }
        url = reverse('profile')
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["success"], False)
        self.assertTrue(test_response_schema(data))

    def test_create_profile_with_valid_data(self):
        self.auth(self.user2)
        data = {
            "can_share_PI": True,
            "address": "28 Boms avenue, Elekahia Port Harcourt",
        }
        url = reverse('profile')
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["status"], 201)
        self.assertEqual(data["success"], True)
        self.assertTrue(test_response_schema(data))

    def test_update_profile_with_invalid_data(self):
        self.auth(self.user)
        data = {
            "phone_number": "+25475845879",
            "x_url": "http://x.com/skhdjfd"
        }
        url = reverse('profile')
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(len(data["errors"]), 2)
        self.assertTrue(test_response_schema(data))

    def test_update_profile_with_valid_data(self):
        self.auth(self.user)
        data = {
            "phone_number": "+233 45467940",
            "occupation": "Profesional Code tester",
        }
        url = reverse('profile')
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(test_response_schema(data))


class QuestionnaireTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="password123",
            first_name="Test",
            last_name="User",
            username=generate_random_username(),
            role="admin"
        )
        self.user2 = User.objects.create_user(
            email="test2@gmail.com",
            password="password123",
            first_name="Test",
            last_name="User",
            username=generate_random_username()
        )
        self.questionnaire = Questionnaire.objects.create(
         **{
            "has_experience_programming": True,
            "worked_on_real_life_problems": True,
            "reason_for_joining_Internpulse": "To be a hell of a tester",
            "importance_of_work_exp": "It allows me to make complete testings",
        }   
        )

    def auth(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {str(refresh.access_token)}')

    def test_create_questionnaire_with_invalid_data(self):
        data = {
            "has_experience_programming": "kshdf",
        }
        url = reverse('questionnaire')
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["success"], False)
        self.assertTrue(test_response_schema(data))

    def test_create_questionnaire_with_valid_data(self):
        self.auth(self.user)
        data = {
            "has_experience_programming": True,
            "worked_on_real_life_problems": True,
            "reason_for_joining_Internpulse": "To be a hell of a tester",
            "importance_of_work_exp": "It allows me to make complete testings",
        }
        url = reverse('questionnaire')
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["status"], 201)
        self.assertEqual(data["success"], True)
        self.assertTrue(test_response_schema(data))

    def test_get_questionnaire_existing(self):
        self.auth(self.user)
        url = reverse('questionnaire-get', kwargs={'id': self.questionnaire.id})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(test_response_schema(data))

    def test_get_questionnaire_not_existing(self):
        self.auth(self.user)
        url = reverse('questionnaire-get', kwargs={'id': 93876366834})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["status"], 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(test_response_schema(data))

    def test_get_questionnaire_without_permissions(self):
        self.auth(self.user2)
        url = reverse('questionnaire-get', kwargs={'id': self.questionnaire.id})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data["status"], 403)
        self.assertEqual(data["success"], False)
        self.assertTrue(test_response_schema(data))
    

    def test_delete_questionnaire_without_permissions(self):
        self.auth(self.user2)
        url = reverse('questionnaire-get', kwargs={'id': self.questionnaire.id})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data["status"], 403)
        self.assertEqual(data["success"], False)
        self.assertTrue(test_response_schema(data))

    def test_delete_questionnaire_with_permissions(self):
        self.auth(self.user)
        url = reverse('questionnaire-get', kwargs={'id': self.questionnaire.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


class UserListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="james@gmail.com",
            password="password123",
            first_name="James",
            last_name="john",
            username=generate_random_username()
        )
        self.auth(self.user)

    def add_users(self, count=10):
        # Create additional users for pagination testing
        for i in range(count):
            User.objects.create_user(
                email=f"user{i+1}@gmail.com",
                password="password123",
                first_name=f"User{i+1}",
                last_name="Test",
                username=generate_random_username()
            )

    def auth(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {str(refresh.access_token)}')

    def test_user_list_authenticated(self):
        url = reverse('user-list')
        self.add_users(2)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(test_response_schema(data, True))
        self.assertIn("page_info", data)
        self.assertIsInstance(data["data"], list)

    def test_user_list_unauthenticated(self):
        self.client.credentials()  # Remove authentication credentials
        url = reverse('user-list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["status"], 401)
        self.assertEqual(data["success"], False)
        self.assertTrue(test_response_schema(data))

    def test_user_list_pagination(self):
        self.add_users(10)
        url = reverse('user-list')
        params = {'page': 2}
        response = self.client.get(url, params)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["status"], status.HTTP_200_OK)
        self.assertEqual(data["success"], True)
        self.assertIn("page_info", data)
        self.assertTrue(test_response_schema(data, True))
        self.assertIsInstance(data["data"], list)
        self.assertIn("next", data["page_info"])
        self.assertIn("previous", data["page_info"])
        self.assertIn("count", data["page_info"])

    def test_user_list_filter_by_first_name(self):
        self.add_users(3)
        url = reverse('user-list')
        query_params = {'first_name': 'james'}
        response = self.client.get(url, query_params)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["status"], status.HTTP_200_OK)
        self.assertEqual(data["success"], True)
        self.assertTrue(test_response_schema(data, True))
        self.assertIn("page_info", data)
        self.assertIsInstance(data["data"], list)
        self.assertEqual(len(data["data"]), 1)
        self.assertIn("next", data["page_info"])
        self.assertIn("previous", data["page_info"])
        self.assertIn("count", data["page_info"])
        for user in data["data"]:
            self.assertEqual(user["first_name"], "James")

    def test_user_list_filter_by_last_name(self):
        self.add_users(2)
        url = reverse('user-list')
        query_params = {'last_name': 'john'}
        response = self.client.get(url, query_params)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["status"], status.HTTP_200_OK)
        self.assertEqual(data["success"], True)
        self.assertTrue(test_response_schema(data, True))
        self.assertIn("page_info", data)
        self.assertIsInstance(data["data"], list)
        self.assertEqual(len(data["data"]), 1)
        self.assertIn("next", data["page_info"])
        self.assertIn("previous", data["page_info"])
        self.assertIn("count", data["page_info"])
        # Assert that all returned users have the specified last name
        for user in data["data"]:
            self.assertEqual(user["last_name"], "john")

    def test_user_list_filter_by_email(self):
        self.add_users(3)
        url = reverse('user-list')
        query_params = {'email': 'user1@gmail.com'}
        response = self.client.get(url, query_params)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["status"], status.HTTP_200_OK)
        self.assertEqual(data["success"], True)
        self.assertTrue(test_response_schema(data, True))
        self.assertIn("page_info", data)
        self.assertIsInstance(data["data"], list)
        self.assertIn("next", data["page_info"])
        self.assertEqual(len(data["data"]), 1)
        self.assertIn("previous", data["page_info"])
        self.assertIn("count", data["page_info"])
        # Assert that all returned users have the specified email
        for user in data["data"]:
            self.assertEqual(user["email"], "user1@gmail.com")


class QuestionnaireListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="james@gmail.com",
            password="password123",
            first_name="James",
            last_name="john",
            username=generate_random_username(),
            role="admin"
        )
        self.auth(self.user)

    def add_qs(self, count=10, idx=False):
        for i in range(count):
            if idx == i:
                Questionnaire.objects.create(
                    **{
                        "has_experience_programming": True,
                        "worked_on_real_life_problems": True,
                        "reason_for_joining_Internpulse": generate_random_username(),
                        "importance_of_work_exp": generate_random_username(),
                    },
                    user = self.user
                )
            else:
                Questionnaire.objects.create(
                    **{
                        "has_experience_programming": True,
                        "worked_on_real_life_problems": True,
                        "reason_for_joining_Internpulse": generate_random_username(),
                        "importance_of_work_exp": generate_random_username(),
                    }
                )

    def auth(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {str(refresh.access_token)}')

    def test_qs_list_authenticated(self):
        url = reverse('questionnaire-list')
        self.add_qs(2)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(test_response_schema(data, True))
        self.assertIn("page_info", data)
        self.assertIsInstance(data["data"], list)

    def test_qs_list_unauthorized(self):
        self.user.role = "intern"
        self.user.save()
        self.add_qs(1)
        url = reverse('questionnaire-list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data["status"], 403)
        self.assertEqual(data["success"], False)
        self.assertTrue(test_response_schema(data))

    def test_qs_list_pagination(self):
        self.add_qs(10)
        url = reverse('questionnaire-list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["success"], True)
        self.assertIn("page_info", data)
        self.assertTrue(test_response_schema(data, True))
        self.assertIsInstance(data["data"], list)
        self.assertIn("next", data["page_info"])
        self.assertIn("previous", data["page_info"])
        self.assertIn("count", data["page_info"])

    def test_qs_list_filter_by_first_name(self):
        self.add_qs(3, 1)
        url = reverse('questionnaire-list')
        query_params = {'first_name': 'james'}
        response = self.client.get(url, query_params)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["status"], status.HTTP_200_OK)
        self.assertEqual(data["success"], True)
        self.assertTrue(test_response_schema(data, True))
        self.assertIn("page_info", data)
        self.assertIsInstance(data["data"], list)
        self.assertEqual(len(data["data"]), 1)
        self.assertIn("next", data["page_info"])
        self.assertIn("previous", data["page_info"])
        self.assertIn("count", data["page_info"])


    def test_qs_list_filter_by_last_name(self):
        self.add_qs(2, 1)
        url = reverse('questionnaire-list')
        query_params = {'last_name': 'john'}
        response = self.client.get(url, query_params)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["status"], status.HTTP_200_OK)
        self.assertEqual(data["success"], True)
        self.assertTrue(test_response_schema(data, True))
        self.assertIn("page_info", data)
        self.assertIsInstance(data["data"], list)
        self.assertEqual(len(data["data"]), 1)
        self.assertIn("next", data["page_info"])
        self.assertIn("previous", data["page_info"])
        self.assertIn("count", data["page_info"])


class LogoutTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="password123",
            first_name="Test",
            last_name="User",
            username=generate_random_username()
        )
        self.refresh_token = RefreshToken.for_user(self.user)

    def auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {str(self.refresh_token.access_token)}')

    def test_logout_with_valid_refresh_token(self):
        self.auth()
        url = reverse('logout')
        response = self.client.post(url, {'refresh': str(self.refresh_token)})
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["message"], "Logout successful")
        self.assertTrue(test_response_schema(data))

    def test_logout_without_refresh_token(self):
        self.auth()
        url = reverse('logout')
        response = self.client.post(url)
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["success"], False)
        self.assertTrue(test_response_schema(data))

    def test_logout_with_invalid_refresh_token(self):
        self.auth()
        url = reverse('logout')
        response = self.client.post(url, {'refresh': 'invalid_token'})
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Validation failed")
        self.assertTrue(test_response_schema(data))

    def test_logout_without_authentication(self):
        url = reverse('logout')
        response = self.client.post(url, {'refresh': str(self.refresh_token)})
        data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["status"], 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not authorized")
        self.assertTrue(test_response_schema(data))



class RefreshTokenTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="password123",
            first_name="Test",
            last_name="User",
            username=generate_random_username()
        )
        self.refresh_token = RefreshToken.for_user(self.user)

    def auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {str(self.refresh_token.access_token)}')

    def test_refresh_token_with_valid_refresh_token(self):
        self.auth()
        url = reverse('refresh-token')
        response = self.client.post(url, {'refresh': str(self.refresh_token)})
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["success"], True)
        self.assertIn("access", data["data"])
        self.assertIn("refresh", data["data"])
        self.assertTrue(test_response_schema(data))

    def test_refresh_token_without_refresh_token(self):
        self.auth()
        url = reverse('refresh-token')
        response = self.client.post(url)
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["success"], False)
        self.assertTrue(test_response_schema(data))

    def test_refresh_token_with_invalid_refresh_token(self):
        self.auth()
        self.refresh_token.blacklist()
        url = reverse('refresh-token')
        response = self.client.post(url, {'refresh': str(self.refresh_token)})
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["status"], 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Validation failed")
        self.assertTrue(test_response_schema(data))

    def test_refresh_token_without_authentication(self):
        url = reverse('refresh-token')
        response = self.client.post(url, {'refresh': str(self.refresh_token)})
        data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["status"], 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not authorized")
        self.assertTrue(test_response_schema(data))
