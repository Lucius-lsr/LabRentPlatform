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
        apply = UpgradeApply.objects.get(applicant__username='user_v1')
        apply.state = 1
        apply.save()

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
        apply = OnShelfApply.objects.get(target_equipment__name="THU")
        apply.state = 1
        apply.save()

    def test_off_shelf(self):
        self.test_on_shelf()
        THU_id = Equipment.objects.get(name="THU").id
        response = self.client.post(
            '/api/v2/offshelf',
            {
                'equipment_id': THU_id
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Equipment.objects.filter(name="THU")), 0)

    def test_borrow_apply(self):
        self.test_on_shelf()
        self.logout()
        self.test_login_v1()
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
        response = self.client.get(
            '/api/v1/applylist',
        )
        self.assertEqual(response.status_code, 200)
        posts = json.loads(response.content)['posts']
        self.assertNotEqual(len(posts), 0)

        self.logout()
        self.test_login_v2()
        response = self.client.get(
            '/api/v2/borrowapplylist',
        )
        self.assertEqual(response.status_code, 200)
        apply = BorrowApply.objects.get(borrower__username='user_v1', owner__username='user_v2')
        self.assertEqual(apply.state, 0)

        response = self.client.get('/api/v2/lendlist')
        posts = json.loads(response.content)
        self.assertEqual(len(posts['posts']), 0)

        response = self.client.put(
            '/api/v2/whether/agree',
            "id={}&flag={}".format(apply.id, 1)
        )
        self.assertEqual(response.status_code, 200)
        apply = BorrowApply.objects.get(id=apply.id)
        self.assertEqual(apply.state, 1)

        response = self.client.get('/api/v2/lendlist')
        posts = json.loads(response.content)
        self.assertNotEqual(len(posts['posts']), 0)

        self.logout()
        self.test_login_v1()
        response = self.client.get('/api/v1/borrowlist')
        self.assertEqual(response.status_code, 200)
        posts = json.loads(response.content)['posts']
        self.assertNotEqual(len(posts), 0)

        self.logout()
        self.test_login_v2()
        response = self.client.put(
            '/api/v2/confirm',
            "id={}".format(apply.id)
        )
        self.assertEqual(response.status_code, 200)
        apply = BorrowApply.objects.get(id=apply.id)
        self.assertEqual(apply.state, 3)


    def test_equipment(self):
        self.test_on_shelf()
        response = self.client.get(
            '/api/v1/search',
            {
                'name': 'THU',
                'page': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            '/api/v1/search',
            {
                'username': 'user_v2',
                'page': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            '/api/v2/equipmentlist',
            {
                'page': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        equipment = Equipment.objects.get(name="THU")
        response = self.client.put(
            '/api/v2/edit',
            "id={}&name={}&description={}&count={}".format(
                equipment.id,
                "PKU",
                "THU to PKU",
                99
            )
        )
        self.assertEqual(response.status_code, 200)
        equipment = Equipment.objects.get(name="PKU")
        self.assertEqual(equipment.count, 99)
        response = self.client.post(
            '/api/v2/increase',
            {
                'id': equipment.id,
                'count': 2
            }
        )
        # print(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        equipment = Equipment.objects.get(name="PKU")
        self.assertEqual(equipment.count, 101)
        response = self.client.post(
            '/api/v2/decrease',
            {
                'id': equipment.id,
                'count': 2
            }
        )
        equipment = Equipment.objects.get(name="PKU")
        self.assertEqual(equipment.count, 99)

    def test_message(self):
        self.test_login_v1()
        response = self.client.post(
            '/api/v1/sendmessage',
            {
                'receiver_name': 'user_v2',
                'content': "message from v1 to v2"
            }
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/v1/getmessages')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['total'], 1)
        self.assertEqual(json.loads(response.content)['new_message'], 0)

        self.logout()
        self.test_login_v2()
        response = self.client.get('/api/v1/getmessages')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['total'], 1)
        self.assertEqual(json.loads(response.content)['new_message'], 1)
        response = self.client.put('/api/v1/readmessages')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1/getmessages')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['total'], 1)
        self.assertEqual(json.loads(response.content)['new_message'], 0)

