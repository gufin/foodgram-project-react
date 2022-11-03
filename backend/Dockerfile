FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .
RUN apt update && apt install fonts-indic -y && fc-cache -f
RUN apt-get update; apt-get install -y fontconfig
RUN fc-cache -f -v
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]