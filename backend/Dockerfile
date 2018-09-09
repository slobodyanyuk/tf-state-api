FROM alpine:3.8
MAINTAINER Slobodianiuk Sergii ssv.lklm@gmail.com
RUN apk add --no-cache \
        uwsgi-python3 \
        python3
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /app
CMD [ "uwsgi", "--socket", "0.0.0.0:3031", \
               "--uid", "uwsgi", \
               "--plugins", "python3", \
               "--master", "--processes", "1", "--threads", "4", \
               "--protocol", "uwsgi", \
               "--file", "wsgi.py" ]
