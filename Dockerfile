FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "api.main:api", "--host", "0.0.0.0", "--port", "8000"]