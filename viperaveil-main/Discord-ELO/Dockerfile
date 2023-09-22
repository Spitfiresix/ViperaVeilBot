FROM python:3.11.0-alpine
LABEL maintainer="Vipera Veil"
LABEL version="0.1"
LABEL description="Vipera Veil ELO Bot"

ENV VVToken="token"

WORKDIR /app

COPY . .

RUN apk update
RUN apk add gcc musl-dev linux-headers g++ tesseract-ocr py3-numpy jpeg-dev zlib-dev libjpeg make
RUN pip install -r ./viperaelo/requirements.txt

CMD [ "python", "./viperaelo/main.py" ]