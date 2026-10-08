FROM python:3.14

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY app/ /app/app/
COPY alembic.ini /app/
COPY alembic/ /app/alembic/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]