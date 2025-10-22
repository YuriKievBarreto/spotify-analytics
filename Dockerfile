# 1. Base Image
FROM python:3.13-slim


WORKDIR /usr/src/app


COPY pyproject.toml poetry.lock ./

RUN pip install poetry


RUN poetry install --no-root 


COPY . .


CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
