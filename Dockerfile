FROM python:3.13

ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root

COPY . /app

EXPOSE 8000


CMD ["/bin/sh", "-c", "poetry run gunicorn --workers 1 --bind 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker app.main:app"]
