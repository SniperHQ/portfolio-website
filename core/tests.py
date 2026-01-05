from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from .models import About, ContactMessage, HeroSection, Skill
from django.core.files.uploadedfile import SimpleUploadedFile

class CoreViewsTests(TestCase):

    def setUp(self):
        # Create test data
        self.client = Client()
        self.hero = HeroSection.objects.create(
            name="Mcondisi",
            title="Web Developer",
            description="Test Hero Section",
            is_active=True
        )

        # About with PDF CV
        self.cv_file = SimpleUploadedFile("test_cv.pdf", b"Dummy PDF content", content_type="application/pdf")
        self.about = About.objects.create(
            title="About Me",
            description="Test description",
            cv=self.cv_file
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.hero.title)

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.about.title)

    def test_download_cv(self):
        response = self.client.get(reverse('download_cv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Disposition').split(';')[0], 'attachment')

    def test_contact_post(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Hello!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(ContactMessage.objects.filter(email='test@example.com').exists())
