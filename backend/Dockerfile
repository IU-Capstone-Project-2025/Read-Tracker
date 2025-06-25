FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh

ENTRYPOINT ["./wait-for-it.sh", "database:5432", "--timeout=30", "--strict", "--"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
