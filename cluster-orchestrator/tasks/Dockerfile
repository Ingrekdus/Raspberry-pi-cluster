FROM arm64v8/alpine:latest

WORKDIR /app

COPY stress-cpu.sh .

RUN chmod +x stress-cpu.sh

CMD ["/app/stress-cpu.sh"]
