FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
RUN ["chmod", "777", "/app/scripts.sh"]
ENTRYPOINT ["/app/scripts.sh"]
