FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/api/alembic.ini .
COPY apps/api/alembic ./alembic
COPY apps/api/app ./app
COPY pytest.ini .
COPY apps/api/tests ./apps/api/tests
COPY tests ./tests
COPY packages ./packages

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
