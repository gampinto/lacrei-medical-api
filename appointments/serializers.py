from django.utils import timezone
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from .models import Appointment, Professional


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Profissional válido",
            summary="Exemplo de profissional",
            description="Dados usados para cadastrar um profissional.",
            value={
                "social_name": "Maria Silva",
                "profession": "Cardiologista",
                "address": "Rua das Flores, 100",
                "contact": "21999999999",
            },
            request_only=True,
        ),
    ]
)
class ProfessionalSerializer(serializers.ModelSerializer):
    social_name = serializers.CharField(
        allow_blank=True,
        help_text="Nome social do profissional.",
    )
    profession = serializers.CharField(
        allow_blank=True,
        help_text="Profissão ou especialidade do profissional.",
    )
    address = serializers.CharField(
        allow_blank=True,
        help_text="Endereço do profissional.",
    )
    contact = serializers.CharField(
        allow_blank=True,
        help_text="Telefone ou outro meio de contato.",
    )

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


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Consulta válida",
            summary="Exemplo de consulta",
            description="Consulta vinculada a um profissional.",
            value={
                "date": "2099-10-03T14:30:00Z",
                "professional": 1,
            },
            request_only=True,
        ),
    ]
)
class AppointmentSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(
        input_formats=[
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M%z",
        ],
        error_messages={
            "invalid": (
                "Informe uma data válida no formato "
                "YYYY-MM-DDTHH:MM:SS+HH:MM."
            )
        },
        help_text="Data e hora futura da consulta.",
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