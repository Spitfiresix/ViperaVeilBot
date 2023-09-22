FROM python:3.11.0-alpine
LABEL maintainer="Vipera Veil"
LABEL version="0.1"
LABEL description="Vipera Veil Discord Connector"

ENV VVToken="token"

EXPOSE 8765
EXPOSE 20000

WORKDIR /app

COPY . .

#RUN apt-get update && apt-get upgrade -y
#RUN apt-get install ffmpeg -y
#RUN export PYTHONPATH=/usr/bin/python
RUN apk update
RUN apk add gcc
RUN apk add g++
RUN apk add libffi-dev
RUN apk add libc-dev
RUN apk add python3-dev
RUN apk add ffmpeg
RUN apk add ffmpeg-libs
RUN apk add opus-dev
RUN apk add postgresql-dev
RUN apk add git
RUN apk add gifsicle
RUN pip install -r requirements.txt
RUN pip install ./viperaveil/wheels/linux/psutil-5.9.4-cp311-abi3-linux_x86_64.whl
RUN pip install ./viperaveil/wheels/linux/vosk-0.3.45-py3-none-linux_x86_64.whl
# RUN echo 'manylinux1_compatible = True' > /usr/local/lib/python3.11/site-packages/_manylinux.py
# RUN python -c 'import sys; sys.path.append(r"/_manylinux.py")'
RUN cp -r ./viperaveil/dependencies/vosk /usr/local/lib/python3.11/site-packages/vosk
#RUN pip install ./wheels/linux/lxml-4.9.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_24_x86_64.whl
RUN pip install lxml

CMD [ "python", "main.py" ]