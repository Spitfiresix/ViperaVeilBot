FROM python:3.11.0-alpine
LABEL maintainer="VierpaVeil"
LABEL version="0.1"
LABEL description="ViperaVeil Website/DBConnector"

WORKDIR /app

EXPOSE 5000

COPY . .

RUN apk add build-base
RUN apk add postgresql-dev
RUN pip install -r requirements.txt
RUN pip install lxml

CMD [ "python", "main.py" ]