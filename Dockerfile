FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false
RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH="$POETRY_HOME/bin:$PATH"

# Diretório da aplicação
WORKDIR /app

# Copiar apenas arquivos de dependência primeiro
COPY pyproject.toml poetry.lock* ./

# Instalar dependências do projeto
RUN poetry install --no-interaction --no-root

# Agora copiar o restante do código
COPY . .

# Expor porta 80
EXPOSE 80

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
