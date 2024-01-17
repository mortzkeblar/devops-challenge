FROM python:3.13.0a2-alpine3.19

WORKDIR /src

RUN pip3 install flask

ENV FLASK_APP=app.py

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]


