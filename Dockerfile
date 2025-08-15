# Dockerfile
FROM python:3.9-slim-buster
WORKDIR / app
COPY pi_worker.py .
ENTRYPOINT ["python", "pi_worker.py"]
CMD ["${SAMPLES}"]
