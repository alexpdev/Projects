FROM python:alpine3.13

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN mkdir /ftp_root
RUN mkdir /ftp_root/nobody
RUN mkdir /ftp_root/user
RUN mkdir /ftp_root/admin

EXPOSE 20:21

CMD python3 runserver.py
