from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from cells.models import ShopCellModel,ProfileUserModel
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

# Test 

class UserApiTestCase(APITestCase):
    
    def setUp(self) -> None:
        self.client_auth = APIClient()
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
       
        self.user2_token,_ = Token.objects.get_or_create(user=self.user2)
         
        ProfileUserModel.objects.create(user=self.user,phone='56364624')
        ProfileUserModel.objects.create(user=self.user2,phone='53634324')
        
        self.item1 = ShopCellModel.objects.create(owner_user=self.user,profile=self.user.profile,
            model_name='TestModel1',price=300,description='User test 1'
        )
        self.item2 = ShopCellModel.objects.create(owner_user=self.user2,profile=self.user2.profile,
            model_name='TestModel2',price=300,description='User test 2'
        )

#*********************************** Test Login ***********************************************************
    def test_login_post(self) -> None:
        response = self.client.post('/api/login/',data={'username':self.user,'password':'12345'})
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
    
    def test_login_post_fail(self) -> None:
        response = self.client.post('/api/login/',data={'username':'TestUser','password':'12345'})
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)
    
    def test_login_post_fail2(self) -> None:
        user = User.objects.create_user(username='UserNoActive',password='12345',
                                        email='usrnoactive@example.com',is_active=False)
        response = self.client.post('/api/login/',data={'username':user.username,'password':'12345'})
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)
    
    def test_login_post_fail3(self) -> None:
        response = self.client.post('/api/login/',data={'username':self.user2.username,'password':'12345'})
        self.assertEqual(response.status_code,status.HTTP_409_CONFLICT)
 
#*********************************** Test Logout **************************************************************
    def test_logout_get(self) -> None:
        user = User.objects.create_user(
            username='TestLogin3',first_name='Test',
            last_name='Login',email='testlogin3@example.com',
            password='12345',is_active=True
        )
        token,_ = Token.objects.get_or_create(user=user)
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client_auth.get('/api/logout/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_logout_get_fail(self) -> None:
        response = self.client.get('/api/logout/')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

#************************************ Test Register *****************************************************************
    def test_register_post(self) -> None:
        response = self.client.post('/api/register/',data={
            'username':'UserRegister','first_name':'User','last_name':'Register',
            'email':'userregister@example.com','password':'12345','password2':'12345',
            'phone':'53634215'
        })
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    def test_register_post_fail(self) -> None:
        response = self.client.post('/api/register/',data={
            'username':self.user.username,'first_name':'User','last_name':'Register',
            'email':'userregister@example.com','password':'12345','password2':'12345',
            'phone':'53634215'
        })
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_register_post_fail2(self) -> None:
        response = self.client.post('/api/register/',data={
            'username':'UserR2','first_name':'User','last_name':'Register',
            'email':self.user2.email,'password':'12345','password2':'12345',
            'phone':'53634215'
        })
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_register_post_fail3(self) -> None:
        response = self.client.post('/api/register/',data={
            'username':'UserR3','first_name':'User','last_name':'Register',
            'email':'user3@example.com','password':'12346','password2':'12345',
            'phone':'53634215'
        })
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

#********************************** Test Item Profile ***************************************************************
    def test_itemprofile_post(self) -> None:
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client_auth.post('/api/item-profile/',data={
            'model_name':'ItemUser','price':300,'image':'','description':'Item User 1'
        })
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    def test_itemprofile_put(self) -> None:
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        pk = str(self.item2.pk) 
        response = self.client_auth.put('/api/item-profile/?pk='+pk,data={
            'model_name':'ItemUpdated','price':305,'image':'','description':'Item User 1 updated'
        })
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
    
    def test_itemprofile_delete(self) -> None:
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        pk = str(self.item2.pk) 
        response = self.client_auth.delete('/api/item-profile/?pk='+pk)
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
    
    def test_itemprofile_put_fail(self) -> None:
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        pk = str(self.item1.pk)
        response = self.client_auth.put('/api/item-profile/?pk='+pk,data={
            'model_name':'ItemUpdated','price':305,'image':'','description':'Item User 1 updated'
        })
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    def test_itemprofile_delete_fail(self) -> None:
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        pk = str(self.item1.pk)
        response = self.client_auth.delete('/api/item-profile/?pk='+pk)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

#************************************ Test Show Item *************************************************************
    def test_showitemprofile_get(self) -> None:
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client_auth.get('/api/profile/show-items/?page=1&search='+self.item2.model_name)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_showitemprofile_get_fail(self) -> None:
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token ' )
        response = self.client_auth.get('/api/profile/show-items/?page=1&search='+self.item2.model_name)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

#************************************* Test Profile ****************************************************************
    def test_profile_get(self) -> None:
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client_auth.get('/api/profile/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_profile_put(self) -> None:
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client_auth.put('/api/profile/',data={
            'username':'UserAPI2new','first_name':'UserAPI2','last_name':'new',
            'email':'userapi2new@example.com','phone':'53634234','image':'','address':'User api 2 new'
        })
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
    
    def test_profile_delete(self) -> None:
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client_auth.delete('/api/profile/')
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
    
    def test_profile_get_fail(self) -> None:
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_profile_put_fail(self) -> None:
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token 8d878dfd9fd7f9d7f9d7ffde')
        response = self.client_auth.get('/api/profile/',data={
            'username':'UserAPI2new','first_name':'UserAPI2','last_name':'new',
            'email':'userapi2new@example.com','phone':'53634234','image':'','address':'User api 2 new'
        })
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_profile_delete_fail(self) -> None:
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token ')
        response = self.client_auth.delete('/api/profile/')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

#*************************************** Test Change Password ****************************************************
    def test_changepassword_put(self) -> None:
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client_auth.put('/api/profile/change-password/',data={
            'currentpassword':'12345','newpassword':'password01','confirmpassword':'password01'
        })
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_changepassword_put_fail(self) -> None:
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client_auth.put('/api/profile/change-password/',data={
            'currentpassword':'12345','newpassword':'password02','confirmpassword':'password01'
        })
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)
    
    def test_changepassword_put_fail2(self) -> None:
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client_auth.put('/api/profile/change-password/',data={
            'currentpassword':'nada456','newpassword':'password02','confirmpassword':'password02'
        })
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

#********************************************* Test Restore Password *************************************************
    def test_restorepassword_post(self) -> None:
        response = self.client.post('/api/restore-password/',data={
            'email':self.user.email
        })
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
    
    def test_restorepassword_post_fail(self) -> None:
        response = self.client.post('/api/restore-password/',data={
            'email':'emptyuser@example.com'
        })
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    
    def test_restorepassword_post_fail2(self) -> None:
        response = self.client.post('/api/restore-password/',data={
            'email':''
        })
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

#****************************************** Test Token link *********************************************************
    def test_tokenlink_get(self) -> None:
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.get('/api/profile/changed-password/'+uid+'/'+token+'/')
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
    
    def test_tokenlink_get_fail(self) -> None:
        response = self.client.get('/api/profile/changed-password/56ff6drtr789rtdf/64fdfdfe6/')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)