FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --default-timeout=100 -r requirements.txt

COPY . .

ENV PYTHONPATH="/app"

CMD ["uvicorn", "part_1.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
