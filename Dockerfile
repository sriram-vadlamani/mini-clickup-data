FROM python:3.10-slim as builder
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
