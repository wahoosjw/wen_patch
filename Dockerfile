FROM python:slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get -y install git

COPY ./start.sh .

CMD [ "./start.sh" ]
