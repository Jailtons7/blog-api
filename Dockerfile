FROM python:3.10

ENV LANG pt-BR.utf8
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000
