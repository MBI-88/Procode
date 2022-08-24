from django.test import TestCase, Client

# Test view

class TestViews(TestCase):

    def setUp(self) -> None:
        self.view_client = Client(HTTP_USER_AGENT='Mozilla/5.0')
    
    # Index view
    def test_index(self) -> None:
        request = self.view_client.get('/index/')
        self.assertEqual(request.status_code, 200)
        self.assertContains(response=request,text='<!--Modal-->',html=True)
    
    # Info view
    def test_info(self) -> None:
        request = self.view_client.get('/info/')
        self.assertEqual(request.status_code, 200)
        self.assertContains(response=request,text='<!--Info-->',html=True)
    
    # Contact view
    def test_contact(self) -> None:
        request = self.view_client.get('/contact/')
        self.assertEqual(request.status_code, 200)
        self.assertContains(response=request,text='<!--Contact-->',html=True)
    
    # Who view
    def test_who(self) -> None:
        request = self.view_client.get('/who/')
        self.assertEqual(request.status_code, 200)
        self.assertContains(response=request,text='<!--Who are we-->',html=True)
    
