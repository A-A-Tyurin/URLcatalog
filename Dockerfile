FROM python:3.10.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD gunicorn run:app --bind 0.0.0.0:5000