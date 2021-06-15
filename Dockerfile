FROM python:3.8.5

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY server.py ./
COPY sym_wrapper.py ./
COPY catp.py ./
COPY createdb.sql ./
COPY db_interaction.py /.

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get install sqlite3 libsqlite3-dev
RUN sqlite3 main.db < createdb.sql

CMD [ "python", "./server.py" ]