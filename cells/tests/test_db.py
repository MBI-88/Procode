from django.test import TestCase
from cells.models import ProfileUserModel,ShopCellModel
from django.contrib.auth.models import User

# Test Data base

class TestUserModel(TestCase):
    
    def setUp(self) -> None:
        self.user_db = User.objects.create(
            username='TestUser',password='password01',
            first_name='Test1',last_name='User1',email='testuser@example.com'
        )
        ProfileUserModel.objects.create(
            user=self.user_db,
            phone='56634324',
            address='Mi direccion user1'
        )
        self.item = ShopCellModel.objects.create(
            owner_user=self.user_db,
            profile=self.user_db.profile,
            model_name='Samsung Test',
            price=250,
            image='',
            description='Item test case'
        )
        self.user_db2 = User.objects.create(
            username='TestUser2',
            password='password01',
            first_name='UserModel2',
            last_name='Model2',
            email='testuser2@example.com'
        )
        ProfileUserModel.objects.create(
            user=self.user_db2,
            phone='53634221',
            address='Mi direccion user2'
        )
    
    def test_usermodel(self) -> None:
        user1 = User.objects.get(username='TestUser')
        user2 = User.objects.get(username='TestUser2')
        self.assertEqual(user1.username,'TestUser')
        self.assertEqual(user1.first_name,'Test1')
        self.assertEqual(user1.last_name,'User1')
        self.assertNotEqual(user1.username,user2.username)
        self.assertEqual(user1.profile.phone,'56634324')
        self.assertNotEqual(user2.profile.address,'Mi direccion user1')
    
    def test_shopcell(self) -> None:
        self.assertNotEqual(self.item.owner_user.username,'TestUser2')
       