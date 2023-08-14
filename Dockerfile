FROM python:3.11.4-alpine3.18

ENV PIP_DISABLE_PIP_VERISON_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /AppToDo

COPY . /AppToDo/

RUN pip install psycopg2-binary

RUN pip install -r requirements.txt
