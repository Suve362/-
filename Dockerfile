FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    ncat awscli curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false
WORKDIR /app/
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
COPY . .

FROM python:3.12-slim AS final
RUN apt-get update && apt-get install -y --no-install-recommends \
    ncat curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /app/
COPY --from=builder /usr/local/ /usr/local/
COPY --from=builder /app/ ./
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
EXPOSE 5002
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]


