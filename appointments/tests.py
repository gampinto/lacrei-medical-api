from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Professional


class ProfessionalAPITests(APITestCase):
    def setUp(self):
        # Credenciais fictícias usadas exclusivamente nos testes automatizados.
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        self.client.force_authenticate(user=self.user)

        self.professional_data = {
            "social_name": "Maria Silva",
            "profession": "Cardiologista",
            "address": "Rua das Flores, 100",
            "contact": "21999999999",
        }

    def test_create_professional(self):
        response = self.client.post(
            "/api/professionals/",
            self.professional_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Professional.objects.count(), 1)
        self.assertEqual(
            response.data["social_name"],
            "Maria Silva",
        )

    def test_list_professionals(self):
        Professional.objects.create(**self.professional_data)

        response = self.client.get("/api/professionals/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_reject_blank_social_name(self):
        invalid_data = self.professional_data.copy()
        invalid_data["social_name"] = ""

        response = self.client.post(
            "/api/professionals/",
            invalid_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("social_name", response.data)