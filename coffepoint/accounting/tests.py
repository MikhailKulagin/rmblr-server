from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Shelf, Cup, CupMaterials, Material

User = get_user_model()


class CoffepointTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим записи в тестовой БД
        User.objects.create(username='test_username', id=1)
        Shelf.objects.create(id=999,
                             number='test_shelf')
        Material.objects.create(id=999,
                                title='Glass')
        Cup.objects.create(id=999,
                           owner_id=1,
                           shelf_id=999,
                           volume=5)
        CupMaterials.objects.create(id=999,
                                    cup_id=999,
                                    material_id=999)

    def setUp(self):
        self.owner_name = 'test_username'
        self.shelf = 'test_shelf'
        self.authorized_client = Client()

    def test_accounting_template(self):
        response = self.authorized_client.get(reverse('accounting:index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_users_template(self):
        response = self.authorized_client.get(reverse('accounting:users', args=[self.owner_name]))
        self.assertTemplateUsed(response, 'user.html')

    def test_accounting_context(self):
        response = self.authorized_client.get(reverse('accounting:index'))
        shelves = response.context.get('shelves')
        owner_name = response.context.get('owner_name')
        shelf_name = [_ for _ in shelves][0]
        self.assertEqual(shelf_name, self.shelf)
        self.assertEqual(owner_name, None)
        self.assertEqual(len(shelves), 1)

    def test_users_context(self):
        response = self.authorized_client.get(reverse('accounting:users', args=[self.owner_name]))
        shelves = response.context.get('shelves')
        owner_name = response.context.get('owner_name')
        self.assertTemplateUsed(response, 'user.html')
        shelf_name = [_ for _ in shelves][0]
        self.assertEqual(shelf_name, self.shelf)
        self.assertEqual(owner_name, self.owner_name)
        self.assertEqual(len(shelves), 1)

