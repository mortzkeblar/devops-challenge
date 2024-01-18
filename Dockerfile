FROM python:3.9-alpine3.18

WORKDIR /src

RUN apk add build-base

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5555

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:5555", "--chdir", "src/", "app:app" ]


