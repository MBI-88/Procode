from django.test import TestCase
from models import ProfileUserModel,ShopCellModel
from django.contrib.auth.models import User

# Test Data base

class TestUserModel(TestCase):
    
    def setUp(self) -> None:
        User.objects.create(
            username='TestUser1',
            password=User.set_password('password1'),
            first_name='UserModel1',
            last_name='Model1',
            email='testuser1@example.com'
        )
        User.objects.create(
            username='TestUser2',
            password=User.set_password('password1'),
            first_name='UserModel2',
            last_name='Model2',
            email='testuser2@example.com'
        )
    
    def test_usermodel(self) -> None:
        user1 = User.objects.get(username='TestUser1')
        user2 = User.objects.get(username='TestUser2')

        self.assertEqual(user1.username,'TestUser1')
        self.assertEqual(user1.first_name,'UserModel1')
        self.assertEqual(user1.last_name,'Model1')
        self.assertFalse(user1.username,user2.username)

        ProfileUserModel.objects.create(
            user=user1,
            phone='56634324',
            image='',
            address='Mi direccion user1'
        )
        ProfileUserModel.objects.create(
            user=user2,
            phone='53634221',
            image='',
            address='Mi direccion user2'
        )
        self.assertEqual(user1.profile.phone,'56634324')
        self.assertFalse(user2.profile.address,'Mi direccion user1')
    
    def test_shoppingcell(self) -> None:
        user1 = User.objects.get(username='TestUser1')
        ShopCellModel.objects.create(
            owner_user=user1,
            profile=user1.profile,
            model_name='Item test',
            price=250,
            image='',
            description='Item test case'
        )
        self.assertEqual(user1.shopcell.model_name,'Item test')
        self.assertFalse(user1.shopcell.price,300)
        item = ShopCellModel.objects.get(model_name='Item test')
        self.assertFalse(item.owner_user.username,'TestUser2')