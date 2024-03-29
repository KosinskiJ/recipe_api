from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase) :

    def setUp(self) :
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@admin.com',
            password = 'admin'

        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'test@test.com',
            password = 'test',
            name = 'Test user'
        )

    def test_user_listed(self) :
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self) :
        """user edit page works"""
        url = reverse('admin:core_user_change', args = [self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_page_create(self) :
        """create user page works"""

        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
