from django.utils import timezone
from rest_framework import serializers

from .models import Appointment, Professional


class ProfessionalSerializer(serializers.ModelSerializer):
    social_name = serializers.CharField(allow_blank=True)
    profession = serializers.CharField(allow_blank=True)
    address = serializers.CharField(allow_blank=True)
    contact = serializers.CharField(allow_blank=True)

    class Meta:
        model = Professional
        fields = ["id", "social_name", "profession", "address", "contact"]

    def validate_social_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "O nome social não pode ficar vazio."
            )

        return value

    def validate_profession(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "A profissão não pode ficar vazia."
            )

        return value

    def validate_address(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "O endereço não pode ficar vazio."
            )

        return value

    def validate_contact(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "O contato não pode ficar vazio."
            )

        return value
    
class AppointmentSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(
        input_formats=[
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M%z",
        ],
        error_messages={
            "invalid": "Informe uma data válida no formato YYYY-MM-DDTHH:MM:SS+HH:MM."
        },
    )

    class Meta:
        model = Appointment
        fields = ["id", "date", "professional"]

    def validate_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                "A consulta deve ser agendada para uma data futura."
            )

        return value