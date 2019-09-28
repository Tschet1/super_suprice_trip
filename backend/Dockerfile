FROM python:3.7
WORKDIR /code
RUN apt-get update && apt-get install -y gdal-bin
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt