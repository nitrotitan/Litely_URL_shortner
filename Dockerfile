#
FROM python:3.11.3-bullseye
WORKDIR /litely

COPY ./requirements.txt /litely/requirements.txt
COPY ./app /litely/app
COPY ./migrations /litely/migrations
COPY ./alembic.ini /litely/alembic.ini
COPY ./manage.py /litely/manage.py

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /litely/requirements.txt

EXPOSE 8080

CMD ["uvicorn", "app.main:fast", "--host", "0.0.0.0", "--port", "2700"]