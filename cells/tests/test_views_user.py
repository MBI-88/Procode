from django.test import TestCase, Client
from django.contrib.auth.models import User
from models import ShopCellModel,ProfileUserModel

        
# Test User

class TestViewsUser(TestCase):

    def setUp(self) -> None:
        self.user_client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.user = User.objects.create(
            username='TestUser',first_name='UserFirst',last_name='UserLast',
            password=User.set_password('password1'),email='testuser@example.com'
        )
        ProfileUserModel.objects.create(user=self.user,phone='58987848')
        self.user2 = User.objects.create(
            username='TestUser2',first_name='UserFirst2',last_name='UserLast2',
            password=User.set_password('password1'),email='testuser2@example.com'
        )
        ProfileUserModel.objects.create(user=self.user2,phone='5363324')
    
    def test_login(self) -> None:
        # True case
        request = self.user_client.get('/login/')
        self.assertEqual(request.status_code,200)
        self.assertContains(response=request,text="<form method='POST' id='login'>",html=True)
        request = self.user_client.post('/login/',data={'username':self.user.username,'password':self.user.password})
        self.assertEqual(request.content,b'302')

        # False case
        request = self.user_client.post('/login/',data={'username':'XxX','password':'xXx1024'})
        self.assertEqual(request.status_code,200)
    
    def test_register(self) -> None:
        # True case
        request = self.user_client.get('/register/')
        self.assertEqual(request.status_code,200)
        self.assertContains(response=request,text="<form method='POST' id='register'>",html=True)
        request = self.user_client.post(
            '/register/',
            data= {
                'username':'UserTestCase',
                'first_name':'Userfirst',
                'last_name':'Userlast',
                'password':'password1',
                'email':'usertestcase@example.com',
                'phone':'54643424'
            }
        )
        self.assertEqual(request.content,b'302')

        # False case
        request = self.user_client.post(
            '/register/',
            data={
                'username':self.user.username,
                'first_name':'UserError',
                'last_name':'UserErrorLong',
                'password':'password1',
                'email':'usererror@example.com',
                'phone':'55652535'
            }
        )
        self.assertEqual(request.status_code,200)

        request = self.user_client.post(
            '/register/',
            data={
                'username':'UserTestCase',
                'first_name':'UserError',
                'last_name':'UserErrorLong',
                'password':'password1',
                'email':self.user.email,
                'phone':'55652535'
            }
        )
        self.assertEqual(request.status_code,200)
    
    def test_user_active(self) -> None:
        self.assertTrue(self.user.is_active)
        user_noActive = User.objects.get(username='UserTestCase')
        self.assertFalse(user_noActive.is_active)

    def test_profile_update(self) -> None:
        request = self.user_client.post('/login/',data={'username':self.user.username,'password':self.user.password})
        # True case
        request = self.user_client.get('/update/profile/')
        self.assertEqual(request.status_code,200)
        self.assertContains(response=request,text='<form method="POST"  enctype="multipart/form-data" action="">')
        request = self.user_client.post(
            '/update/profile/',
            data={
                'username':self.user.username,
                'first_name':self.user.first_name,
                'last_name':self.user.last_name,
                'email':'usertestcase@example.com',
                'phone':'58987842',
                'image':'',
                'address':'Playa e/ 5ta y 42 edif 128'
            }
        )
        self.assertEqual(request.status_code,302)

        # False case
        self.user.is_active = True
        self.user.save()
        request = self.user_client.post('/login/',data={'username':self.user.username,'password':self.user.password})
        request = self.user_client.post(
            '/update/profile/',
            data={
                'username':self.user.username,
                'first_name':self.user.first_name,
                'last_name':self.user.last_name,
                'email':'smart2055@yahoo.com', # E-mail is iqual to other e-mail in the data base
                'phone':'58987842',
                'image':'',
                'address':'Playa e/ 5ta y 42 edif 128'
            }
        )
        self.assertEqual(request.status_code,200)

    
    def test_create_item(self) -> None:
        request = self.user_client.post('/login/',data={'username':self.user.username,'password':self.user.password})
        # True case
        request = self.user_client.get('/create/item/')
        self.assertEqual(request.status_code, 200)
        self.assertContains(response=request,
        text='<form method="POST" id="createitem" enctype="multipart/form-data" action="">',html=True)
        request = self.user_client.post(
            '/create/item/',
            data={
                'model_name':'ItemTestCase',
                'price':200,
                'image':'',
                'description':'Item of test case'
            }
        )
        self.assertEqual(request.status_code, 302)
        request = self.user_client.get('/logout/')
        self.assertEqual(request.status_code, 302)

    def test_update_item(self) -> None:
        item = ShopCellModel.objects.get(model_name='ItemTestCase')
        request = self.user_client.post('/login/',
                                            data={'username':self.user.username,'password':self.user.password})
        # True case
        request = self.user_client.get('/update/item/'+item.pk+'/')
        self.assertEqual(request.status_code, 200)
        self.assertContains(response=request,
            text='<form method="POST"  enctype="multipart/form-data" action="">',html=True)
        request = self.user_client.post(
            '/update/item/'+item.pk+'/',
            data={
                'model_name':'ItemTestCase Updated',
                'price':300,
                'image':'',
                'description':'Item test case updated'
            }
        )
        self.assertEqual(request.status_code, 302)
        request = self.user_client.get('/logout/')
        self.assertEqual(request.status_code, 302)

        # False case
        request = self.user_client.post('/login/',
                            data={'username':self.user2.username,'password':self.user2.password})
        request = self.user_client.post(
            '/update/item/'+item.pk+'/',
            data={
                'model_name':'ItemTestCase2 Updated',
                'price':300,
                'image':'',
                'description':'Item test case updated 2'
            }
        )
        self.assertEqual(request.status_code, 200)
        request = self.user_client.get('/logout/')
        self.assertEqual(request.status_code, 302)

    def test_delete_item(self) -> None:
        request = self.user_client.post('/login/',
                                        data={'username':self.user.username,'password':self.user.password})
        item = ShopCellModel.objects.create(
            owner_user=self.user,profile=self.user.profile,
            model_name='ItemTestCase-Delete',price=500,image='',description='Item test casde deleted'
        )
        
        # True case
        request = self.user_client.get('/delete/item/'+item.pk+'/')
        self.assertEqual(request.status_code, 200)
        self.assertContains(response=request,
                            text='<form method="POST" id="deleteitem" action="" data-pk={} >'.format(item.pk))
        request = self.user_client.post('/delete/item/'+item.pk+'/',data={'delete':True})
        self.assertEqual(request.status_code, 302)
        request = self.user_client.get('/logout/')
        self.assertEqual(request.status_code, 302)

        # False case
        request = self.user_client.post('/login/',
                                        data={'username':self.user2.username,'password':self.user2.password})
        item = ShopCellModel.objects.get(model_name='ItemTestCase Updated')
        request = self.user_client.post('/delete/item/'+item.pk+'/',data={'delete':True},follow=True)
        self.assertEqual(request.status_code, 200)
        self.assertContains(response=request,text='<!--Message-->',html=True)
        request = self.user_client.get('/logout/')
        self.assertEqual(request.status_code, 302)

    def test_change_password(self) -> None:
        request = self.user_client.post('/login/',
                                        data={'username':self.user.username,'password':self.user.password})
        # True case
        request = self.user_client.get('/register/changepassword/')
        self.assertEqual(request.status_code, 200)
        self.assertContains(response=request,text='<form method="POST" id="changepassword">',html=True)
        request = self.user_client.post('/register/changepassword/',
                                        data={
                                            'currentpassword':self.user.password,
                                            'newpassword':'password01',
                                            'confirmpassword':'password01'
                                        }
                                    )
        self.assertEqual(request.content, b'302')

        # False case
        request = self.user_client.post('/login/',
                                        data={'username':self.user2.username,'password':self.user2.password})
        request = self.user_client.post('/register/changepassword/',
                                        data={
                                            'currentpassword':self.user2.password,
                                            'newpassword':self.user2.password,
                                            'confirmpassword':'password01'
                                        }
                                    )
        self.assertEqual(request.status_code, 200)

    def test_delete_user(self) -> None:
        request = self.user_client.post('/login/',
                                        data={'username':self.user2.username,'password':self.user2.password})
        request = self.user_client.get('/delete/profile/')
        self.assertEqual(request.status_code, 200)
        self.assertContains(response=request,text='<form method="POST" action="" id="deleteprofile" >',html=True)
        request = self.user_client.post('/delete/profile/',data={'delete':True})
        self.assertEqual(request.content, b'302')
    
    def test_restore_password(self) -> None:
        # True case
        request = self.user_client.get('/restore/password/')
        self.assertEqual(request.status_code, 200)
        self.assertContains(response=request,text='<form method="POST" id="restorepassword">',html=True)
        request = self.user_client.post('/restore/password/',data={'email':self.user.email})
        self.assertEqual(request.content, b'302')

        # False case
        request = self.user_client.post('/restore/password/',data={'email':'notexits@example.com'})
        self.assertEqual(request.status_code, 200)





        
    

    



        