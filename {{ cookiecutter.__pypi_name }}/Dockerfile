FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python -u -m {{ cookiecutter.__pypi_name }}
