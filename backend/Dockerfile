FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .
RUN apt update
RUN apt install fonts-indic -y
RUN apt-get update
RUN apt-get install -y fontconfig
RUN fc-cache -f -v
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]