from django.test import TestCase,Client
from django.contrib.auth.models import User
from cells.models import ShopCellModel,ProfileUserModel

        
# Test User

class TestViewsUser(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='TestUser',first_name='Test',last_name='User',
            email='testuser@example.com',password='password01'
        )
        self.user1.save()
        ProfileUserModel.objects.create(user=self.user1,phone='58987848')
        
        self.user2 = User.objects.create_user(
            username='TestUser2',first_name='Tests',last_name='User',
            email='testuser2@example.com',password='password1'
        )
        self.user2.save()
        ProfileUserModel.objects.create(user=self.user2,phone='5363324')

        ShopCellModel.objects.create(
            owner_user=self.user1,profile=self.user1.profile,
            model_name='ItemTestCase Delete',price=500,description='Item test casde deleted'
        )
    
    def test_login_get(self) -> None:
        response = self.client.get('/cells/login/')
        self.assertContains(response,text='<!--Login-->',count=1)
    
    def test_login_post(self) -> None:
        login = self.client.login(username=self.user1.username,password=self.user1.password)
        self.assertTrue(login)
        
    def test_login_fail(self) -> None:
        login = self.client.login(username='Empty',password='empty')
        self.assertFalse(login)

    def test_register(self) -> None:
        response = self.client.get('/cells/register/')
        self.assertContains(response,text="<!--Register-->",count=1)
    
    def test_register_post(self) -> None:
        response = self.client.post(
            '/cells/register/',
            data= {
                'username':'UserTestCase',
                'first_name':'Userfirst',
                'last_name':'Userlast',
                'password':'password01',
                'password2':'password01',
                'email':'usertestcase@example.com',
                'phone':'54643424'
            }
        )
        self.assertEqual(response.content,b'302')

    def test_register_fail(self) -> None:
        response = self.client.post(
            '/cells/register/',
            data={
                'username':'TestUser',
                'first_name':'UserError',
                'last_name':'UserErrorLong',
                'password':'password1',
                'email':'usererror@example.com',
                'phone':'55652535'
            }
        )
        self.assertEqual(response.status_code,200)
        response = self.client.post(
            '/cells/register/',
            data={
                'username':'UserTestXX',
                'first_name':'UserError',
                'last_name':'UserErrorLong',
                'password':'password1',
                'email':'testuser@example.com',
                'phone':'55652535'
            }
        )
        self.assertEqual(response.status_code,200)

    def test_user_active(self) -> None:
        user = User.objects.get(username='TestUser')
        self.assertTrue(user.is_active)
        user = User.objects.filter(username='UserTestCase').first()
        # No active
        self.assertIsNone(user)

    def test_profile_update(self) -> None:
        self.client.force_login(User.objects.get(username=self.user1.username))
        response = self.client.get('/cells/update/profile/')
        self.assertContains(response,text='<!--Update profile-->',count=1)
       
    def test_profile_update_post(self) -> None:
        self.client.force_login(User.objects.get(username=self.user1.username))
        response = self.client.post(
            '/cells/update/profile/',
            data={
                'username':'LXA25',
                'first_name':'TU1',
                'last_name':'User1',
                'email':'testuser@example.com',
                'phone':'58987842',
                'image':'',
                'address':'Playa e/ 5ta y 42 edif 128'
            },format='multipart'
        )
        self.assertEqual(response.status_code,302)
    
    def test_profile_update_post_fail(self) -> None:
        self.client.force_login(User.objects.get(username=self.user1.username))
        response = self.client.post(
            '/cells/update/profile/',
            data={
                'username':self.user1.username,
                'first_name':self.user1.first_name,
                'last_name':self.user1.last_name,
                'email':self.user2.email, # E-mail is iqual to other e-mail in the data base
                'phone':'58987842',
                'image':'',
                'address':'Playa e/ 5ta y 42 edif 128'
            }
        )
        self.assertEqual(response.status_code,200)
        self.client.logout()

    def test_create_item(self) -> None:
        self.client.force_login(User.objects.get(username=self.user1.username))
        request = self.client.get('/cells/create/item/')
        self.assertContains(response=request,text='<!--Create item-->',count=1)
        self.client.logout()

    def test_create_item_post(self) -> None:
        self.client.force_login(User.objects.get(username=self.user1.username))
        response = self.client.post(
            '/cells/create/item/',
            data={
                'model_name':'ItemTestCase',
                'price':200,
                'image':'',
                'description':'Item of test case'
            }
        )
        self.assertEqual(response.status_code, 302)
        request = self.client.get('/cells/logout/') # Prube logout view
        self.assertEqual(request.status_code, 302)

    def test_update_item(self) -> None:
        self.client.force_login(User.objects.get(username=self.user1.username))
        item = ShopCellModel.objects.get(model_name='ItemTestCase')
        pk = str(item.pk)
        response = self.client.get('/cells/update/item/'+pk+'/')
        self.assertContains(response,text='<!--Update item-->',count=1)
        self.client.logout()

    def test_update_item_post(self) -> None:
        self.client.force_login(User.objects.get(username=self.user1.username))
        item = ShopCellModel.objects.get(model_name='ItemTestCase')
        pk = str(item.pk)
        response = self.client.post(
            '/cells/update/item/'+pk+'/',
            data={
                'model_name':'ItemTestCase Updated',
                'price':300,
                'image':'',
                'description':'Item test case updated'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    def test_update_item_post_fail(self) -> None:
        self.client.force_login(User.objects.get(username=self.user2.username))
        item = ShopCellModel.objects.get(model_name='ItemTestCase Updated')
        pk = str(item.pk)
        response = self.client.post(
            '/cells/update/item/'+pk+'/',
            data={
                'model_name':'ItemTestCase2 Updated',
                'price':300,
                'image':'',
                'description':'Item test case updated 2'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_delete_item(self) -> None:
        self.client.force_login(User.objects.get(username=self.user1.username))
        item = ShopCellModel.objects.get(model_name='ItemTestCase-Delete')
        pk = str(item.pk)
        response = self.client.get('/cells/delete/item/'+pk+'/')
        self.assertContains(response,text='<!--Delete item-->',count=1)

    def test_delete_item_post(self) -> None:
        self.client.force_login(User.objects.get(username=self.user1.username))
        item = ShopCellModel.objects.get(model_name='ItemTestCase-Delete')
        pk = str(item.pk)
        response = self.client.post('/cells/delete/item/'+pk+'/',data={'delete':True})
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    def test_delete_item_post_fail(self) -> None:
        self.client.force_login(User.objects.get(username=self.user2.username))
        item = ShopCellModel.objects.get(model_name='ItemTestCase Updated')
        pk = str(item.pk)
        response = self.client.post('/cells/delete/item/'+pk+'/',data={'delete':True})
        self.assertContains(response,text='<!--Message-->',count=1)
        self.client.logout()

    def test_change_password(self) -> None:
        self.client.force_login(User.objects.get(username=self.user1.username))
        response = self.client.get('/cells/register/changepassword/')
        self.assertContains(response,text='<!--Change password-->',count=1)
        
    def test_change_password_post(self) -> None:
        self.client.force_login(User.objects.get(username=self.user1.username))
        response = self.client.post('/cells/register/changepassword/',
                                    data={
                                        'currentpassword':self.user1.password,
                                        'newpassword':'password02',
                                        'confirmpassword':'password02'
                                    }
                                )
        
        self.assertEqual(response.content, b'302')

    def test_change_password_post_fail(self) -> None:
        self.client.force_login(User.objects.get(username=self.user2.username))
        response = self.client.post('/cells/register/changepassword/',
                                        data={
                                            'currentpassword':self.user2.password,
                                            'newpassword':self.user2.password,
                                            'confirmpassword':'password2'
                                        }
                                    )
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self) -> None:
        self.client.force_login(User.objects.get(username=self.user1.username))
        response = self.client.get('/cells/delete/profile/')
        self.assertContains(response,text='<!--Delete account-->',count=1)

    def test_delete_user_post(self) -> None:
        self.client.force_login(User.objects.get(username=self.user2.username))
        response = self.client.post('/cells/delete/profile/',data={'delete':True})
        self.assertEqual(response.content, b'302')
    
    def test_restore_password(self) -> None:
        response = self.client.get('/cells/restore/password/')
        self.assertContains(response,text='<!--Restore password-->',count=1)
    
    def test_restore_password_post(self) -> None:
        response = self.client.post('/cells/restore/password/',data={'email':self.user1.email})
        self.assertEqual(response.content, b'302')

    def test_restore_password_post_fail(self) -> None:
        response = self.client.post('/cells/restore/password/',data={'email':'notexits@example.com'})
        self.assertEqual(response.status_code, 200)





        
    

    



        