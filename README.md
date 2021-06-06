# SymbServer

Client-server application for symbolical differentiation and integration using SymPy library. Based on sockets python interface usage.

All recipes for running app are for Linux based OS.

Developed on Ubuntu 20.04 using Python 3.8.5 and Docker version 20.10.6, build 370c289.

SymbServer uses [CATP protocol](docs/CATP.md) to transfer information through TCP connection.

## Run locally

Python 3 should be installed to use both client and server part of app.

All required packages can be found in *requirements.txt* and can be installed by running in project directory:

```bash
pip install --no-cache-dir -r requirements.txt
```
To run server and client you can use:

```bash
sudo python3 server.py
```

```bash
sudo python3 client.py
```
***SUDO IS NECESSARY***

## Run using container

All the commands should be run from the respective folder.

`server` folder contains Dockerfile which can be used to build and run containerized version of server app.

First of all you need to build Docker image from Dockerfile by using in project directory:

```bash
docker build -t symb_server -f Dockerfile.server .
```
Then you can run built container image using:

```bash
docker run --name sserver --net=host -it symb_server:latest
```

It works absolutely the same way with client application.

`client` folder contains Dockerfile which can be used to build and run containerized version of client app.

First of all you need to build Docker image from Dockerfile by using in project directory:

```bash
docker build -t symb_client -f Dockerfile.client .
```
Then you can run built container image using:

```bash
docker run --name sclient --net=host -it symb_client:latest
```

## Usage guide

### Server

Server will print you some information about its work process such as info about:
- start of server (IPv4, port, time of start)
- connection to the server
- recieved message
- sent message to client
- availability for new connection

### Client

Client application is fully text/CLI-based.

To use client app appropriately first of all you should choose mode. Mode 
can be chosen in each request to the app separately.
By now there are 4 modes:

|Mode name|Mode description|
|---|---|
|   |   |
|   |   |
|   |   |