#
FROM python:3.10.8-slim-buster

#
WORKDIR /litely

#
COPY ./requirements.txt ./litely/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r ./litely/requirements.txt

#
COPY ./migrations ./litely/migrations
#
CMD ["python"," manage.py","-db", "migrate"]
#
CMD ["python"," manage.py","-db", "upgrade"]
#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0","--proxy-headers", "--port", "80"]
