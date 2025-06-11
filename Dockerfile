FROM python:3.11-slim
WORKDIR /app
COPY HelloWorld.py .
CMD ["python", "HelloWorld.py"]