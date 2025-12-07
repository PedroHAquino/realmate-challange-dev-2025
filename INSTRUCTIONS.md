# INSTRUCTIONS.md

Este documento contém todas as instruções necessárias para instalar, executar e testar o projeto do desafio Realmate.

---

# 📦 Pré-requisitos

Antes de iniciar, você precisa ter instalado:

- Docker
- Docker Compose
- Git

> **Observação:** Não é necessário instalar Python, Poetry ou dependências manualmente.  
> Todo o ambiente é configurado automaticamente dentro dos containers.

---

# 🚀 Como rodar o projeto

## 1️⃣ Clonar o repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd realmate-challenge
```

---

## 2️⃣ Subir os containers

O comando abaixo constrói a imagem, instala tudo via Poetry e sube a aplicação:

```bash
docker compose up --build
```

Isso irá iniciar:

- **web** → container com Django + DRF + Poetry  
- **db** → container com PostgreSQL  

A aplicação ficará disponível em:

```
http://localhost
```

---

# 🧱 Migrações do Banco

Com os containers rodando, execute:

```bash
docker compose exec web python manage.py migrate
```

Isso cria todas as tabelas necessárias para a API.

---

# 🔐 Criar superusuário (opcional)

Caso queira acessar o painel admin:

```bash
docker compose exec web python manage.py createsuperuser
```

Acesse:

```
http://localhost/admin/
```

---

# 🌐 Endpoints da API

## 📍 1. Webhook — POST `/webhook/`

Este endpoint recebe os eventos enviados pelo sistema externo e processa:

Tipos aceitos:

- `NEW_CONVERSATION`
- `NEW_MESSAGE`
- `CLOSE_CONVERSATION`

### Exemplo — Criar nova conversa

```json
{
  "type": "NEW_CONVERSATION",
  "timestamp": "2025-02-21T10:20:41.349308",
  "data": { "id": "550e8400-e29b-41d4-a716-446655440000" }
}
```

### Exemplo — Nova mensagem

```json
{
  "type": "NEW_MESSAGE",
  "timestamp": "2025-02-21T10:20:42.349308",
  "data": {
    "id": "9b9b9b9b-1a2b-4c5d-8e9f-1234567890ab",
    "direction": "RECEIVED",
    "content": "Olá, tudo bem?",
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

### Exemplo — Fechar conversa

```json
{
  "type": "CLOSE_CONVERSATION",
  "timestamp": "2025-02-21T10:20:45.349308",
  "data": { "id": "550e8400-e29b-41d4-a716-446655440000" }
}
```

---

## 📍 2. Consultar conversa — GET `/conversation/<uuid>/`

Retorna:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "state": "OPEN",
  "messages": [
    {
      "id": "9b9b9b9b-1a2b-4c5d-8e9f-1234567890ab",
      "direction": "RECEIVED",
      "content": "Olá tudo bem?",
      "timestamp": "2025-02-21T10:20:42.349308"
    }
  ]
}
```

---

# 🗃 Banco de Dados

Este projeto utiliza **PostgreSQL** com as seguintes credenciais:

- **DB:** realmate  
- **USER:** realmate  
- **PASSWORD:** realmate  
- **HOST:** db  
- **PORT:** 5432  

As configurações estão em:

```
docker-compose.yaml
```

E no arquivo `.env` utilizado pela aplicação.

---

# 🛑 Parar os containers

```bash
docker compose down
```

---

# ✔ Projeto pronto para uso

Este projeto atende todos os requisitos obrigatórios do desafio:

- Django + Django REST Framework
- PostgreSQL
- Docker + Docker Compose
- Poetry
- Webhook funcional
- Regras de negócio implementadas
- Endpoint GET de conversas
- INSTRUCTIONS.md