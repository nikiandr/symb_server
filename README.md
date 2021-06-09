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

You can also choose port which server uses to connect to it using command line argument.

```bash
sudo python3 client.py <port>
```
where <port> - port which is used by server.
***SUDO IS NECESSARY***

## Run using container

All the commands should be run from the respective folder.


First of all you need to build Docker image from Dockerfile by using in project directory:

```bash
docker build -t symb_server .
```
Then you can run built container image using:

```bash
docker run --name sserver -p <port>:50 -it symb_server:latest
```
where <port> - port which you want to be used by SymbServer
 
## Usage guide

### Server

Server will print you some information about its work process such as info about:
- start of server (IPv4, port, time of start)
- connection to the server
- received message
- sent message to client
- availability for new connection

### Client

Client application is fully text/CLI-based.

To use client app appropriately first you should choose mode. Mode 
can be chosen in each request to the app separately.
By now there are 4 modes:

|  Packet mode   | Description                                                  |
| :------------: | :----------------------------------------------------------- |
|   derivative   | Computation of derivative or partial derivative of any order of specific function |
|  def_integral  | Computation of definite integral on the interval of function |
| indef_integral | Computation of indefinite integral of function               |
|    simplify    | Simplification of expression                                 |

After choosing method you should basically follow the instructions and that's all.
