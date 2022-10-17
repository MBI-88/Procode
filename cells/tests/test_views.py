from urllib import response
from django.test import TestCase
from cells.models import ShopCellModel,ProfileUserModel
from django.contrib.auth.models import User

# Test view

class TestViews(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            username='UserTestCaseView',password='password01',
            first_name='UserTest',last_name='CaseView',email='testcase@example.com'
        )
        ProfileUserModel.objects.create(user=self.user,phone='54642434')
        ShopCellModel.objects.create(
            profile=self.user.profile,
            model_name='Item test view',price='200'
        )
    
    # Showitems view
    def test_show_items(self) -> None:
        response = self.client.get('/cells/shopping/')
        self.assertContains(response,text='<!--Show Items-->',count=1)
        self.assertContains(response,text='<!--Item Ajax-->',count=1)
    
    # Detailitem view
    def test_detail_item(self) -> None:
        item = ShopCellModel.objects.get(model_name='Item test view')
        pk = str(item.pk)
        request = self.client.get('/cells/shopping/'+pk+'/')
        self.assertContains(response=request,text='<!--Detail item-->',count=1)
    
