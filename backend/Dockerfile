FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV FLASK_APP=app
ENV FLASK_RUN_PORT=5000
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
#CMD ["python", "-m", "unittest", "discover", "tests"]
