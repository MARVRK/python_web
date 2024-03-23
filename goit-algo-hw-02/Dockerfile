FROM python:3.8

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY task_2.py /app/task_2.py

WORKDIR /app

CMD ["python", "-m", "task_2.py"]
