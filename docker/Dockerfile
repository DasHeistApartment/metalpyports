FROM python:3.8

RUN pip install kubernetes

WORKDIR /app

COPY python .

CMD [ "python", "main.py" ]