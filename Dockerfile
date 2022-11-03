#
FROM python:3.11.0-slim-buster

#
WORKDIR root/

#
COPY ./requirements.txt /root /requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /root/requirements.txt

#
COPY ./app /root /app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
