from django.test import TestCase
from .models import *
import json


# Create your tests here.
class UserMethodTest(TestCase):
    def setUp(self):
        # password = blueice
        User.objects.create(
            username='user_v1',
            password=r'pbkdf2_sha256$216000$g4lJOgTwTI14$xTETWjvOcse6DJ07vIN+kJkyBVQOnYzKPQJLY2fofag=',
            email='user1@user1.com',
            is_verified=True
        )
        User.objects.create(
            username='user_v2',
            password=r'pbkdf2_sha256$216000$g4lJOgTwTI14$xTETWjvOcse6DJ07vIN+kJkyBVQOnYzKPQJLY2fofag=',
            email='user2@user2.com',
            is_verified=True,
            is_provider=True
        )
        self.assertEqual(len(User.objects.all()), 2)

    def test_register(self):
        response = self.client.post(
            '/api/v1/register',
            data={
                'username': 'new_user',
                'password': 'new_password',
                'email': 'test@test.com'
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        user = User.objects.get(username='user_v1')
        self.assertIsNotNone(user)
        response = self.client.patch(
            '/api/v1/login',
            "username=user_v1&password=blueice"
        )
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.patch(
            '/api/v1/login',
            "username=user_v1&password=blueice"
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.patch(
            '/api/v1/logout'
        )
        self.assertEqual(response.status_code, 200)

    def test_search_equipment(self):
        response = self.client.patch(
            '/api/v1/login',
            "username=user_v1&password=blueice"
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            '/api/v1/search',
            {
                "name": "THU",
                "page": 1
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_upgrade_apply(self):
        response = self.client.patch(
            '/api/v1/login',
            "username=user_v1&password=blueice"
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.put(
            '/api/v1/upgrade',
            "lab_info=This is an upgrade apply"
        )
        self.assertEqual(response.status_code, 200)
        apply = UpgradeApply.objects.filter(applicant__username='user_v1')
        self.assertNotEqual(len(apply), 0)
        apply = apply[0]
        self.assertEqual(apply.state, 0)
        apply.state = 1
        apply.save()

    def test_on_shelf(self):
        response = self.client.patch(
            '/api/v2/login',
            "username=user_v1&password=blueice"
        )
        self.assertEqual(response.status_code, 200)

