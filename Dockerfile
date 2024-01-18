FROM python:3.9-alpine3.18

WORKDIR /src

RUN apk add build-base

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]


