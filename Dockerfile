FROM python:3.8.13-buster

COPY menu_me /menu_me
COPY requirements.txt /requirements.txt
COPY api /api

RUN pip install -r requirements.txt
RUN pip install -e .

CMD uvicorn api.api:app --host 0.0.0.0 --port $PORT
