FROM python:3.11-slim
RUN pip install --no-cache-dir Pillow
WORKDIR /app
COPY convert.py .
RUN mkdir -p input output
CMD ["python3", "convert.py"]