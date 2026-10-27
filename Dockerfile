FROM python:3.12-slim
WORKDIR /app
COPY app.py .
COPY data/ ./data/
EXPOSE 8080
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/healthz', timeout=2)"
CMD ["python", "-u", "app.py"]
