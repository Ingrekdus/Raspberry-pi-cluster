```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalace závislostí
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopírování aplikace
COPY app.py .

# Exponování portu
EXPOSE 5000

# Spuštění aplikace
CMD ["python", "app.py"]
```
