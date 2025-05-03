FROM python:3.11.8-alpine3.19

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD src /app

WORKDIR /app

CMD ["flask", "run", "--host", "0.0.0.0"]
