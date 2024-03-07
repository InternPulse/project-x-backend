from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from .models import Certificate
from cohort_management.models import InternProfile, Cohort


class CertificateIssueBatchAPIViewTests(TestCase):
    def setUp(self):
        pass
        # Create test users
        # self.user1 = get_user_model().objects.create_user(username='testuser1', email='testuser1@example.com', password='password123')
        # self.user2 = get_user_model().objects.create_user(username='testuser2', email='testuser2@example.com', password='password456')

        # # Create a test cohort
        # self.cohort = Cohort.objects.create(title='Test Cohort', description='Test Description', rules='Test Rules')

        # # Create test intern profiles
        # self.intern1 = InternProfile.objects.create(user=self.user1, cohort=self.cohort, role='Product designer')
        # self.intern2 = InternProfile.objects.create(user=self.user2, cohort=self.cohort, role='Backend developer')

        # # Create a test certificate
        # self.certificate = Certificate.objects.create(title='Test Certificate', description='Test Description', image='media/certificates/dp.png', issued_to='Test Recipient')

        # # Authenticate the test client
        # self.client = APIClient()
        # self.client.force_authenticate(user=self.user1)

    def test_certificate_list_create_endpoint(self):
        url = reverse('certificate-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_certificate_detail_endpoint(self):
        # Assuming you have at least one certificate in the database
        # certificate_id = Certificate.objects.first().id
        url = reverse('certificate-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_certificate_issue_batch_endpoint(self):
        url = reverse('certificate-issue-batch')
        response = self.client.post(url, {})  # Assuming an empty POST request is sufficient for testing
        self.assertEqual(response.status_code, 401)  # Assuming it returns a 400 for missing data
