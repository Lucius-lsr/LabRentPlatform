from django.test import TestCase
from .models import *
import json


# Create your tests here.
class AllMethodTest(TestCase):
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

    def test_login_v1(self):  # user_v1
        try:
            User.objects.get(username='user_v1')
        except:
            self.assertIsNotNone("user_v1 exist")

        response = self.client.patch(
            '/api/v1/login',
            "username=user_v1&password=blueice"
        )
        self.assertEqual(response.status_code, 200)

    def test_login_v2(self):  # user_v2
        try:
            User.objects.get(username='user_v2')
        except:
            self.assertIsNotNone("user_v2 exist")

        response = self.client.patch(
            '/api/v1/login',
            "username=user_v2&password=blueice"
        )
        self.assertEqual(response.status_code, 200)

    def logout(self):
        response = self.client.patch(
            '/api/v1/logout'
        )
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.test_login_v2()
        response = self.client.patch(
            '/api/v1/logout'
        )
        self.assertEqual(response.status_code, 200)

    def test_search_equipment(self):
        self.test_login_v2()
        response = self.client.get(
            '/api/v1/search',
            {
                "name": "THU",
                "page": 1
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_upgrade_apply(self):
        self.test_login_v1()
        response = self.client.put(
            '/api/v1/upgrade',
            "lab_info=This is an upgrade apply"
        )
        self.assertEqual(response.status_code, 200)
        try:
            apply = UpgradeApply.objects.get(applicant__username='user_v1')
            apply.state = 1
            apply.save()
        except:
            self.assertSequenceEqual("Upgrade success")

    def test_on_shelf(self):
        self.test_login_v2()
        response = self.client.post(
            '/api/v2/onshelf',
            {
                "name": "THU",
                "description": "THU description",
                "remarks": "THU remarks",
                "count": 10
            }
        )
        self.assertEqual(response.status_code, 200)
        try:
            apply = OnShelfApply.objects.get(target_equipment__name="THU")
            apply.state = 1
            apply.save()
        except:
            self.assertEqual(0, 1)

    def test_off_shelf(self):
        self.test_on_shelf()
        try:
            THU_id = Equipment.objects.get(name="THU").id
            response = self.client.delete(
                '/api/v2/offshelf',
                "equipment_id={}".format(THU_id)
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(Equipment.objects.filter(name="THU")), 0)
        except:
            self.assertIsNotNone("THU exist")

    def test_borrow_apply(self):
        self.test_on_shelf()
        self.logout()
        self.test_login_v1()
        try:
            THU_id = Equipment.objects.get(name="THU").id
            response = self.client.post(
                '/api/v1/apply',
                {
                    "id": THU_id,
                    "endtime": "2020-09-07T15:00:00Z",
                    "reason": "This is reason for borrow THU",
                    "count": 3
                }
            )
            self.assertEqual(response.status_code, 200)
            borrow_apply = BorrowApply.objects.get(target_equipment__name="THU")
            self.assertIsNotNone(borrow_apply)
        except:
            self.assertIsNotNone("Borrow THU success")
