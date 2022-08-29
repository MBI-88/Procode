from django.test import TestCase, Client
from cells.models import ShopCellModel,ProfileUserModel
from django.contrib.auth.models import User

# Test view

class TestViews(TestCase):

    def setUp(self) -> None:
        self.view_client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.user = User.objects.create(
            username='UserTestCaseView',password='password01',
            first_name='UserTest',last_name='CaseView',email='testcase@example.com'
        )
        ProfileUserModel.objects.create(user=self.user,phone='54642434')
        ShopCellModel.objects.create(
            owner_user=self.user,profile=self.user.profile,
            model_name='Item test view',price='200'
        )
    
    # Index view
    def test_index(self) -> None:
        request = self.view_client.get('/cells/index/')
        self.assertContains(response=request,text='<!--Index-->',count=1)
    
    # Info view
    def test_info(self) -> None:
        request = self.view_client.get('/cells/info/')
        self.assertContains(response=request,text='<!--Info-->',count=1)
    
    # Contact view
    def test_contact(self) -> None:
        request = self.view_client.get('/cells/contact/')
        self.assertContains(response=request,text='<!--Contact-->',count=1)
    
    # Who view
    def test_who(self) -> None:
        request = self.view_client.get('/cells/who/')
        self.assertContains(response=request,text='<!--Who are we-->',count=1)
    
    # Showitems view
    def test_show_items(self) -> None:
        request = self.view_client.get('/cells/shopping/')
        self.assertContains(response=request,text='<!--Show Items-->',count=1)
    
    # Detailitem view
    def test_detail_item(self) -> None:
        item = ShopCellModel.objects.get(model_name='Item test view')
        pk = str(item.pk)
        request = self.view_client.get('/cells/shopping/'+pk+'/')
        self.assertContains(response=request,text='<!--Detail item-->',count=1)
    
