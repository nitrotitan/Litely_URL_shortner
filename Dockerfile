#
FROM python:3.12.0a7-slim-buster

#
WORKDIR /litely

#
# COPY ./requirements.txt /litely/requirements.txt
# COPY ./app /litely/app
#
RUN pip install --no-cache-dir --upgrade -r /litely/requirements.txt
#
# ADD ./migrations /litely/migrations
# ADD ./alembic.ini /litely/alembic.ini
# ADD ./manage.py /litely/manage.py

#
RUN /litely/app/service/setup.py build_ext --inplace
#
EXPOSE 8080
#
CMD ["uvicorn", "app.main:fast", "--host", "0.0.0.0", "--port", "2700"]
