from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

# TODO: при импорте ошибка Model class rmblr-server.coffepoint.accounting.models.Shelf doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.
# from .models import Shelf, Cup, CupMaterials, Material

User = get_user_model()


class CoffepointTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим записи в тестовой БД
        User.objects.create(username='test_username')

    def setUp(self):
        self.user = None
        self.owner_name = 'test_username'
        self.authorized_client = Client()

    def test_accounting_template(self):
        response = self.authorized_client.get(reverse('accounting:index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_users_template(self):
        response = self.authorized_client.get(reverse('accounting:users', args=[self.owner_name]))
        self.assertTemplateUsed(response, 'user.html')

    def test_accounting_context(self):
        # TODO: Сделать, когда получится имортировать модели
        pass

    def test_users_context(self):
        # TODO: Сделать, когда получится имортировать модели
        pass
