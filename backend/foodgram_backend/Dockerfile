FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir
#RUN python3 manage.py upload_ingredients --no-cache-dir

COPY . /app

CMD ["gunicorn", "foodgram_backend.wsgi:application", "--bind", "0:8000"]