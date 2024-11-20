FROM python:3.12-slim

WORKDIR app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE ${COMMAND_APP_PORT} ${QUERY_APP_PORT}
