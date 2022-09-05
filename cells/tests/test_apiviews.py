from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from cells.models import ProfileUserModel,ShopCellModel

# Test

class APIviewsTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='TestLogin',first_name='Test',
            last_name='Login',email='testlogin@example.com',
            password='12345'
        )
        self.user2 = User.objects.create_user(
            username='TestLogin2',first_name='Test',
            last_name='Login',email='testlogin2@example.com',
            password='12345'
        )
        self.user3 = User.objects.create_user(
            username='TestLogin3',first_name='Test',
            last_name='Login',email='testlogin3@example.com',
            password='12345'
        )

        ProfileUserModel.objects.create(user=self.user,phone='56364624')
        ProfileUserModel.objects.create(user=self.user2,phone='53634324')
        ProfileUserModel.objects.create(user=self.user3,phone='53634334')

        self.item1 = ShopCellModel.objects.create(owner_user=self.user,profile=self.user.profile,
            model_name='TestModel1',price=300,description='User test 1'
        )
        self.item2 = ShopCellModel.objects.create(owner_user=self.user2,profile=self.user2.profile,
            model_name='TestModel2',price=300,description='User test 2'
        )
        self.item3 = ShopCellModel.objects.create(owner_user=self.user3,profile=self.user3.profile,
            model_name='TestModel3',price=300,description='User test 3'
        )
    
#******************************* Test Show Items *******************************************************
    def test_showitems_get(self) -> None:
        response = self.client.get('/api/show-items/?page=1')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_showitems_get2(self) -> None:
        response = self.client.get('/api/show-items/?page=1&search='+self.item3.model_name)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_showitems_get_fail(self) -> None:
        response = self.client.get('/api/show-items/?page=hola')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

#*********************************** Test Item Detail *****************************************************
    def test_detailitem_get(self) -> None:
        pk = str(self.item1.pk)
        response = self.client.get('/api/detail/item/'+pk+'/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_detailitem_get_fail(self) -> None:
        response = self.client.get('/api/detail/item/')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

