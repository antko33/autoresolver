FROM python:3.12-slim

WORKDIR app/

COPY requirements/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY bot/ bot/
COPY misc/ misc/
