FROM python:3.12-slim

WORKDIR /app

# Dependências de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala uv corretamente
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copia apenas dependências primeiro (cache melhor)
COPY pyproject.toml uv.lock .python-version ./

# Instala dependências
RUN uv sync --frozen --no-dev

# Agora copia código
COPY . .

EXPOSE 8000

# Execução via uv (mais consistente com seu stack)
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]