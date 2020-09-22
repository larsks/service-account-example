FROM alpine

RUN apk add --update python3 py3-pip uwsgi uwsgi-python3 uwsgi-http

COPY requirements.txt /tmp/requirements.txt
RUN /usr/bin/pip3 install -r /tmp/requirements.txt

COPY . /app
WORKDIR /app
CMD uwsgi --uid=uwsgi --http-socket 0.0.0.0:8080 --master \
	--plugin python3 \
	--mount /=service_account_example:app
