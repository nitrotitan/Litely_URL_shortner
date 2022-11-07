#
FROM python:3.10.8-slim-buster

#
WORKDIR /litely

#
COPY ./requirements.txt /litely/requirements.txt
COPY ./app /litely/app
#
RUN pip install --no-cache-dir --upgrade -r /litely/requirements.txt
#
ADD ./migrations /litely/migrations
ADD ./alembic.ini /litely/alembic.ini
ADD ./manage.py /litely/manage.py

#

#
EXPOSE 8080
#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "2700"]
