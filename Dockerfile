FROM python:3.12-slim

WORKDIR /app

ARG APP_VERSION=Aceestver-3.2.4.py

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY source_versions/ ./source_versions/
COPY tests/ ./tests/

RUN test -f "/app/source_versions/${APP_VERSION}"

ENV APP_VERSION=${APP_VERSION}

CMD ["python", "-c", "import pathlib, py_compile; files=sorted(pathlib.Path('/app/source_versions').glob('*.py')); print('Validating', len(files), 'versions'); [py_compile.compile(str(f), doraise=True) for f in files]; print('All source versions compiled successfully')"]