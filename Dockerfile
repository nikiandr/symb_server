FROM python:3.8.5

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY server.py ./
COPY sym_wrapper.py ./
COPY catp.py ./
COPY createdb.sql ./
COPY dbinteraction.py ./

RUN pip install --no-cache-dir -r requirements.txt
RUN cat /etc/os-release
RUN apt-get update
RUN apt-get -y install apt-utils sqlite3 libsqlite3-dev
RUN sqlite3 main.db < createdb.sql

CMD [ "python", "./server.py" ]