from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

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
            "address": "Rua Inventada, 1",
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

    def test_retrieve_professional(self):
        professional = Professional.objects.create(
            **self.professional_data
        )

        response = self.client.get(
            f"/api/professionals/{professional.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], professional.id)

    def test_update_professional(self):
        professional = Professional.objects.create(
            **self.professional_data
        )

        updated_data = self.professional_data.copy()
        updated_data["profession"] = "Neurologista"

        response = self.client.put(
            f"/api/professionals/{professional.id}/",
            updated_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["profession"],
            "Neurologista",
        )

    def test_delete_professional(self):
        professional = Professional.objects.create(
            **self.professional_data
        )

        response = self.client.delete(
            f"/api/professionals/{professional.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Professional.objects.filter(id=professional.id).exists()
        )


class AppointmentAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        self.client.force_authenticate(user=self.user)

        self.professional = Professional.objects.create(
            social_name="Maria Silva",
            profession="Cardiologista",
            address="Rua das Flores, 100",
            contact="21999999999",
        )

    def test_create_appointment(self):
        response = self.client.post(
            "/api/appointments/",
            {
                "date": "2099-10-03T14:30:00Z",
                "professional": self.professional.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filter_appointments_by_professional(self):
        response = self.client.post(
            "/api/appointments/",
            {
                "date": "2099-10-03T14:30:00Z",
                "professional": self.professional.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(
            f"/api/appointments/?professional={self.professional.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_reject_past_appointment(self):
        response = self.client.post(
            "/api/appointments/",
            {
                "date": "1998-10-03T02:20:00Z",
                "professional": self.professional.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date", response.data)

    def test_reject_nonexistent_professional(self):
        response = self.client.post(
            "/api/appointments/",
            {
                "date": "2099-10-03T14:30:00Z",
                "professional": 999999,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("professional", response.data)

    def test_retrieve_appointment(self):
        create_response = self.client.post(
            "/api/appointments/",
            {
                "date": "2099-10-03T14:30:00Z",
                "professional": self.professional.id,
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            status.HTTP_201_CREATED,
        )

        appointment_id = create_response.data["id"]

        response = self.client.get(
            f"/api/appointments/{appointment_id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], appointment_id)

    def test_update_appointment(self):
        create_response = self.client.post(
            "/api/appointments/",
            {
                "date": "2099-10-03T14:30:00Z",
                "professional": self.professional.id,
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            status.HTTP_201_CREATED,
        )

        appointment_id = create_response.data["id"]

        updated_data = {
            "date": "2099-11-03T15:30:00Z",
            "professional": self.professional.id,
        }

        response = self.client.put(
            f"/api/appointments/{appointment_id}/",
            updated_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["date"],
            "2099-11-03T15:30:00Z",
        )

    def test_delete_appointment(self):
        create_response = self.client.post(
            "/api/appointments/",
            {
                "date": "2099-10-03T14:30:00Z",
                "professional": self.professional.id,
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            status.HTTP_201_CREATED,
        )

        appointment_id = create_response.data["id"]

        response = self.client.delete(
            f"/api/appointments/{appointment_id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class AuthenticationAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Credenciais fictícias usadas exclusivamente nos testes automatizados.
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
        )

    def test_professionals_requires_authentication(self):
        response = self.client.get("/api/professionals/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_professionals(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/professionals/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)