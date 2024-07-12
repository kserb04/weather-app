FROM python:3.12-slim
WORKDIR /home/app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app app
COPY core core
COPY endpoints endpoints
COPY models models
COPY service service
COPY main.py .
