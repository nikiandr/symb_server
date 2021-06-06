# CATP (Computer algebra transfer protocol)
## Description

CATP or Computer algebra transfer protocol is a network protocol is application level protocol 
which can be used to exchange computation requests and responses as well as progress responses.

It is specifically designed to be used for client-server computer algebra systems such as 
SymbServer or WolframAlpha.

## Packet structure

CATP packet consists of two parts: header (first 4 bytes of packet) and content.

### Header

First byte of the packet corresponds to the type of packet. There are three possible modes:

| Packet type |      |      |
| :---------- | :--: | :--: |
|             |      |      |
|             |      |      |
|             |      |      |
