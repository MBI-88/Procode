from django.test import TestCase,Client
from django.contrib.auth.models import User
from cells.models import ShopCellModel,ProfileUserModel

        
# Test Register

class RegisterTestCase(TestCase):

    def test_register(self) -> None:
        response = self.client.get('/cells/register/')
        self.assertEqual(response.status_code,200)
    
    def test_register_post(self) -> None:
        response = self.client.post('/cells/register/',data={
            'username':'TestRegister','first_name':'Test',
            'last_name':'Register','password':'password1',
            'password2':'password1','email':'testuser@example.com',
            'phone':'54643424'
        })
        self.assertEqual(response.content,b'302')

class LoginTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create_user(
            username='TestLogin',first_name='Test',
            last_name='Login',email='testlogin@example.com',
            password='12345'
        )
        return super().setUpTestData()
    
    def test_login(self) -> None:
        response = self.client.get('/cells/login/')
        self.assertContains(response,text='<!--Login-->',count=1)
    
    def test_login_post(self) -> None:
        user = User.objects.get(username='TestLogin')
        response = self.client.post('/cells/login/',data={
            'username':user.username,
            'password':user.password,
        })
        self.assertEqual(response.content,b'302')
        





        
    
    


 







        
    

    



        