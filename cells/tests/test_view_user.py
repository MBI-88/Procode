from django.test import TestCase, Client
from django.contrib.auth.models import User

        
# Test User

class TestUser(TestCase):

    def setUp(self) -> None:
        self.user_client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.user = User.objects.create(
            username='TestUser',first_name='UserFirst',last_name='UserLast',
            password=User.set_password('password1'),email='testuser@example.com'
        )
    
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
                'username':'UserNameTest',
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

    def test_profile(self) -> None:
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
                'email':'start1843@example.com',
                'phone':'58987842',
                'image':'',
                'address':'Playa e/ 5ta y 42 edif 128'
            }
        )
        self.assertEqual(request.status_code,302)

        # False case
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
        pass

    def test_updat_item(self) -> None:
        pass
    
    def test_delete_item(self) -> None:
        pass

    def test_delete_user(self) -> None:
        pass





        
    

    



        