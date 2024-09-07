FROM python:3.12.3

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "food_delivery/manage.py", "runserver", "0.0.0.0:8000"]
