# Lacrei Medical API

API RESTful para gerenciamento de profissionais e consultas médicas, desenvolvida com Django REST Framework, PostgreSQL e Docker. Este projeto não é oficial, feito apenas para treinamento e demonstração de habilidades. Na Branch master haverá apenas o back-end, pedido pela startup, e o projeto será aproveitado para treinamento de front-end em uma branch secundária.

## Tecnologias

- Python 3.12
- Django
- Django REST Framework
- PostgreSQL
- Docker
- Docker Compose
- JWT (Django REST Framework SimpleJWT)
- Poetry

## Funcionalidades

- CRUD de profissionais
- CRUD de consultas
- Associação de consultas a profissionais
- Filtro de consultas por ID do profissional
- Validação dos dados recebidos
- Autenticação JWT
- Testes automatizados
- Ambiente com Docker Compose

## Como executar

### Pré-requisitos

É necessário ter Docker Desktop com integração ao WSL 2.

### Configuração

1) Clone o repositório e entre na pasta do projeto:

git clone https://github.com/gampinto/lacrei-medical-api.git
cd lacrei-medical-api

2) Crie um arquivo .env na raiz do projeto:

SECRET_KEY=sua-chave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=nome_do_banco
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_HOST=db
POSTGRES_PORT=5432

3) Inicie a aplicação:
docker compose up -d --build

4) Verifique os containers:
docker compose ps

5) A API estará disponível no navegador: http://127.0.0.1:8000/

6) O Token de acesso estará disponível em http://127.0.0.1:8000/api/token. É possível gerar um novo token em http://127.0.0.1:8000/api/token/refresh.

7) Para acessar os endpoints protegidos, utilize 
Authorization: Bearer <access_token>

8) Link para uso dos endpoints:
GET    /api/professionals/
POST   /api/professionals/
GET    /api/professionals/{id}/
PUT    /api/professionals/{id}/
PATCH  /api/professionals/{id}/
DELETE /api/professionals/{id}/

9) Filtro por profissional: GET /api/appointments/?professional=1

10) Testes automatizados podem ser automatizados dentro do container Django com:
docker compose exec web poetry run python manage.py test

11) Para encerrar a aplicação, utilize:
docker compose down

