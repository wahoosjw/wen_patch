FROM python:slim

WORKDIR /usr/src/app

COPY ./start.sh .
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get update && apt-get -y install git \
    && chmod 744 ./start.sh

CMD [ "./start.sh" ]
