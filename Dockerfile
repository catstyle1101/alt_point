FROM python:3.11-slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y libpq-dev gcc
WORKDIR /app
COPY requirements.txt .
COPY server_start.sh .
RUN pip install -U pip && pip install -r requirements.txt --no-cache-dir && pip install gunicorn
COPY ./backend/ .
RUN chmod +x server_start.sh
ENTRYPOINT ["/app/server_start.sh"]
