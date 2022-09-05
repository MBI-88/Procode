from telnetlib import STATUS
from django.test import TestCase
from django.contrib.auth.models import User
from cells.models import ShopCellModel,ProfileUserModel
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

        
# Test Register

class ViewUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username='TestLogin',first_name='Test',
            last_name='Login',email='testlogin@example.com',
            password='12345'
        )
        cls.user2 = User.objects.create_user(
            username='TestLogin2',first_name='Test',
            last_name='Login',email='testlogin2@example.com',
            password='12345'
        )

        ProfileUserModel.objects.create(user=cls.user,phone='56364624')
        ProfileUserModel.objects.create(user=cls.user2,phone='53634324')

        cls.item1 = ShopCellModel.objects.create(owner_user=cls.user,profile=cls.user.profile,
            model_name='TestModel1',price=300,description='User test 1'
        )
        cls.item2 = ShopCellModel.objects.create(owner_user=cls.user2,profile=cls.user2.profile,
            model_name='TestModel2',price=300,description='User test 2'
        )
        return super().setUpTestData()

#****************************************** Test Register ***********************************************************
    def test_register(self) -> None:
        response = self.client.get('/cells/register/')
        self.assertContains(response,text='<!--Register-->',count=1)
    
    def test_register_post(self) -> None:
        response = self.client.post('/cells/register/',data={
            'username':'TestRegister','first_name':'Test',
            'last_name':'Register','password':'password1',
            'password2':'password1','email':'testuser@example.com',
            'phone':'54643424'
        })
        self.assertEqual(response.content,b'302')
    
    def test_registe_post_fail(self) -> None:
        response = self.client.post('/cells/register/',data={
            'username':self.user.username,'first_name':'Test',
            'last_name':'Register','password':'password1',
            'password2':'password1','email':'testregisterfail@example.com',
            'phone':'54643424'
        })
        self.assertEqual(response.status_code,200)

        response = self.client.post('/cells/register/',data={
            'username':'TestRegisterFail','first_name':'Test',
            'last_name':'Register','password':'password1',
            'password2':'password1','email':self.user2.email,
            'phone':'54643424'
        })
        self.assertEqual(response.status_code,200)

#****************************************** Test Login **************************************************************
    def test_login(self) -> None:
        response = self.client.get('/cells/login/')
        self.assertContains(response,text='<!--Login-->',count=1)
    
    def test_login_post(self) -> None:
        user = User.objects.get(username='TestLogin')
        response = self.client.post('/cells/login/',data={
            'username':user.username,'password':'12345',
        })
        self.assertEqual(response.content,b'302')
    
    def test_login_post_fail(self) -> None:
        response = self.client.post('/cells/login/',data={
            'username':'NotExists','password':'12345',
        })
        self.assertContains(response,text='<!--Message error-->',count=1)

#********************************************* Test Create Item ********************************************************    
    def test_createitem(self) -> None:
        self.client.force_login(user=self.user)
        response = self.client.get('/cells/create/item/')
        self.assertContains(response,text='<!--Create item-->',count=1)
    
    def test_createitem_post(self) -> None:
        self.client.force_login(user=self.user)
        response = self.client.post('/cells/create/item/',data={
                    'model_name':'TestModel3','price':250,'image':'','description':'Item test'
        })
        self.assertEqual(response.status_code,302)

#********************************************* Test Update item *******************************************************    
    def test_updateitem(self) -> None:
        self.client.force_login(user=self.user)
        pk = str(self.item1.pk)
        response = self.client.get('/cells/update/item/'+pk+'/')
        self.assertContains(response,text='<!--Update item-->',count=1)
    
    def test_updateitem_post(self) -> None:
        self.client.force_login(user=self.user)
        pk = str(self.item1.pk)
        response = self.client.post('/cells/update/item/'+pk+'/',data={
                    'model_name':self.item1.model_name,'price':150,'image':'','description':'Item changed'
        })
        self.assertEqual(response.status_code,302)
    
    def test_updateitem_post_fail(self) -> None:
        self.client.force_login(user=self.user2)
        pk = str(self.item1.pk)
        response = self.client.post('/cells/update/item/'+pk+'/',data={
                    'model_name':self.item1.model_name,'price':150,'image':'','description':'Item changed'
        })
        self.assertContains(response,text='<!--Message-->',count=1)

#********************************************** Test Delete Item *******************************************************    
    def test_deleteitem(self) -> None:
        self.client.force_login(user=self.user2)
        pk = str(self.item2.pk)
        response = self.client.get('/cells/delete/item/'+pk+'/')
        self.assertContains(response,text='<!--Delete item-->',count=1)
    
    def test_deleteitem_post(self) -> None:
        self.client.force_login(user=self.user2)
        pk = str(self.item2.pk)
        response = self.client.post('/cells/delete/item/'+pk+'/',data={'delete':True})
        self.assertEqual(response.status_code,302)
    
    def test_deleteitem_post_fail(self) -> None:
        self.client.force_login(user=self.user2)
        pk = str(self.item1.pk)
        response = self.client.post('/cells/delete/item/'+pk+'/',data={'delete':True},follow=True)
        self.assertContains(response,text='<!--Message-->',count=1)

#********************************************* Test Profile ************************************************************
    def test_profile(self) -> None:
        self.client.force_login(user=self.user)
        response = self.client.get('/cells/profile/')
        self.assertContains(response,text='<!--User information-->',count=1)

#********************************************** Test Update Profile ****************************************************    
    def test_update_profile(self) -> None:
        self.client.force_login(user=self.user)
        response = self.client.get('/cells/update/profile/')
        self.assertContains(response,text='<!--Update profile-->',count=1)
    
    def test_update_profile_post(self) -> None:
        self.client.force_login(user=self.user2)
        image = open('cells/static/img/test_image/Python.png','rb')
        response = self.client.post('/cells/update/profile/',data={
            'username':self.user2,'first_name':'User2Upd','last_name':'Updated','email':'user2upd@example.com',
            'phone':'52223242','image':image,'address':'User updated'
        })
        self.assertEqual(response.status_code,302)
    
    def test_update_profile_post_fail(self) -> None:
        self.client.force_login(user=self.user)
        image = open('cells/static/img/test_image/Python.png','rb')
        response = self.client.post('/cells/update/profile/',data={
            'username':self.user2,'first_name':'User2Upd','last_name':'Updated','email':'user1upd@example.com',
            'phone':'52223242','image':image,'address':'User updated'
        })
        self.assertContains(response,text='<!--Message-->',count=1)

    def test_update_profile_post_fail2(self) -> None:
        self.client.force_login(user=self.user2)
        image = open('cells/static/img/test_image/Python.png','rb')
        response = self.client.post('/cells/update/profile/',data={
            'username':'UserLogged','first_name':'User2Upd','last_name':'Updated','email':self.user.email,
            'phone':'52223242','image':image,'address':'User updated'
        })
        self.assertContains(response,text='<!--Message-->',count=1)

#*********************************************** Test Change Password *************************************************
    def test_changepassword(self) -> None:
        self.client.force_login(user=self.user2)
        response = self.client.get('/cells/register/changepassword/')
        self.assertContains(response,text='<!--Change password-->',count=1)
    
    def test_changepassword_post(self) -> None:
        self.client.force_login(user=self.user2)
        response = self.client.post('/cells/register/changepassword/',data={
            'currentpassword':'12345','newpassword':'password1','confirmpassword':'password1'
        })
        self.assertEqual(response.content,b'302')
    
    def test_changepassword_post_fail(self) -> None:
        self.client.force_login(user=self.user2)
        response = self.client.post('/cells/register/changepassword/',data={
            'currentpassword':'12345','newpassword':'12345','confirmpassword':'password1'
        })
        self.assertContains(response,text='<!--Message-->',count=1)

        response = self.client.post('/cells/register/changepassword/',data={
            'currentpassword':'12345','newpassword':'password01','confirmpassword':'password1'
        })
        self.assertContains(response,text='<!--Message-->',count=1)

#************************************************ Test Restore password *************************************************    
    def test_restore_password(self) -> None:
        response = self.client.get('/cells/restore/password/')
        self.assertContains(response,text='<!--Restore password-->',count=1)
    
    def test_restore_password_post(self) -> None:
        response = self.client.post('/cells/restore/password/',data={
            'email':self.user2.email,
        })
        self.assertEqual(response.content,b'302')
    
    def test_restore_password_post_fail(self) -> None:
        response = self.client.post('/cells/restore/password/',data={
            'email':'nadie@example.com',
        })
        self.assertContains(response,text='<!--Message-->',count=1)

#******************************************** Test Delete Profile *****************************************************
    def test_deleteprofile(self) -> None:
        self.client.force_login(user=self.user2)
        response = self.client.get('/cells/delete/profile/')
        self.assertContains(response,text='<!--Delete account-->',count=1)
    
    def test_deleteprofile_post(self) -> None:
        self.client.force_login(user=self.user2)
        response = self.client.post('/cells/delete/profile/',data={'delete':True})
        self.assertEqual(response.content,b'302')

#******************************************* Test Token link *******************************************************
    def test_tokenlink_get(self) -> None:
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.get('/cells/register/'+uid+'/'+token+'/')
        self.assertEqual(response.status_code,302)
    
    def test_tokenlink_get_fail(self) -> None:
        response = self.client.get('/cells/register/64df4wd56dfd464dfd/dfdfdf4589fdf9e/')
        self.assertContains(response,text='<!--Token fail-->',count=1)






        
    
    


 







        
    

    



        