from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework import viewsets

from .models import Appointment, Professional
from .serializers import AppointmentSerializer, ProfessionalSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Lista profissionais",
        description="Retorna todos os profissionais cadastrados.",
        tags=["Profissionais"],
    ),
    retrieve=extend_schema(
        summary="Consulta um profissional",
        description="Retorna os dados de um profissional específico.",
        tags=["Profissionais"],
    ),
    create=extend_schema(
        summary="Cadastra um profissional",
        description="Cria um novo profissional.",
        tags=["Profissionais"],
        examples=[
            OpenApiExample(
                "Profissional inválido",
                summary="Nome social vazio",
                value={
                    "social_name": "",
                    "profession": "Cardiologista",
                    "address": "Rua das Flores, 100",
                    "contact": "21999999999",
                },
                request_only=True,
            ),
        ],
    ),
    update=extend_schema(
        summary="Atualiza um profissional",
        description="Substitui os dados de um profissional.",
        tags=["Profissionais"],
    ),
    partial_update=extend_schema(
        summary="Atualiza parcialmente um profissional",
        description="Atualiza somente os campos enviados.",
        tags=["Profissionais"],
    ),
    destroy=extend_schema(
        summary="Exclui um profissional",
        description="Remove um profissional cadastrado.",
        tags=["Profissionais"],
    ),
)
class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Lista consultas",
        description=(
            "Retorna as consultas cadastradas. "
            "É possível filtrar pelo ID do profissional."
        ),
        tags=["Consultas"],
        parameters=[
            OpenApiParameter(
                name="professional",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="ID do profissional para filtrar as consultas.",
                examples=[
                    OpenApiExample(
                        "Exemplo",
                        value=1,
                    )
                ],
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Consulta um agendamento",
        description="Retorna uma consulta específica.",
        tags=["Consultas"],
    ),
    create=extend_schema(
        summary="Cadastra uma consulta",
        description="Cria uma nova consulta para um profissional.",
        tags=["Consultas"],
        examples=[
            OpenApiExample(
                "Data inválida",
                summary="Consulta no passado",
                value={
                    "date": "1998-10-03T02:20:00Z",
                    "professional": 1,
                },
                request_only=True,
            ),
            OpenApiExample(
                "Profissional inexistente",
                summary="ID de profissional inválido",
                value={
                    "date": "2099-10-03T14:30:00Z",
                    "professional": 999999,
                },
                request_only=True,
            ),
        ],
    ),
    update=extend_schema(
        summary="Atualiza uma consulta",
        description="Substitui os dados de uma consulta.",
        tags=["Consultas"],
    ),
    partial_update=extend_schema(
        summary="Atualiza parcialmente uma consulta",
        description="Atualiza somente os campos enviados.",
        tags=["Consultas"],
    ),
    destroy=extend_schema(
        summary="Exclui uma consulta",
        description="Remove uma consulta cadastrada.",
        tags=["Consultas"],
    ),
)
class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        queryset = Appointment.objects.all()
        professional_id = self.request.query_params.get("professional")

        if professional_id:
            queryset = queryset.filter(professional_id=professional_id)

        return queryset