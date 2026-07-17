from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from utils.choices import UserRole


class CoreViewsTestCase(TestCase):
    """Test core endpoints like homepage and health checks."""

    def test_homepage_status_code(self) -> None:
        """Verify the homepage renders with 200 OK status."""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kabulhaden CMS")

    def test_health_check_status_code(self) -> None:
        """Verify the health check endpoint returns 200 OK and database status JSON."""
        response = self.client.get(reverse('core:health_check'))
        self.assertEqual(response.status_code, 200)
        
        json_data = response.json()
        self.assertEqual(json_data['status'], 'healthy')
        self.assertEqual(json_data['database'], 'operational')


class CustomUserTestCase(TestCase):
    """Test custom User creation and role assignments."""

    def test_create_user_with_uuid(self) -> None:
        """Verify standard user creation assigns UUID primary key and default role."""
        User = get_user_model()
        user = User.objects.create_user(
            username='editor_test',
            email='editor@kabulhaden.com',
            password='testpassword123'
        )
        self.assertIsNotNone(user.id)
        self.assertEqual(user.role, UserRole.VIEWER)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self) -> None:
        """Verify superuser creation sets proper admin and superuser flags and roles."""
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin@kabulhaden.com',
            password='adminpassword123'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.role, UserRole.SUPERUSER)
