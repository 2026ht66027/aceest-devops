FROM python:3.12-slim

WORKDIR /app

ARG APP_VERSION=Aceestver-3.2.4.py

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY source_versions/ ./source_versions/
COPY tests/ ./tests/

RUN test -f "/app/source_versions/${APP_VERSION}"

ENV APP_VERSION=${APP_VERSION}

CMD ["python", "-c", "import os, py_compile; py_compile.compile('/app/source_versions/' + os.environ['APP_VERSION'], doraise=True); print('Syntax validation successful:', os.environ['APP_VERSION'])"]