# CATP (Computer algebra transfer protocol)
## Description

CATP or Computer algebra transfer protocol is a network protocol is application level protocol
which can be used to exchange computation requests and responses as well as progress responses.

It is specifically designed to be used for client-server computer algebra systems such as
SymbServer or WolframAlpha.

## Versions

| Version | Progress    | Changes                                                      | Documentation                 |
| ------- | ----------- | ------------------------------------------------------------ | ----------------------------- |
| v0.0.1  | Completed   | Created basic protocol                                       | [Documentation](catp/v001.md) |
| v0.0.2  | Completed  | Second byte with content length deleted from header; http-like packet ending: <CR><LF> (that is, a [carriage return](https://en.wikipedia.org/wiki/Carriage_return) character followed by a [line feed](https://en.wikipedia.org/wiki/Line_feed) character); packet types for authentication and history; no bounds on packet length. | [Documentation](catp/v002.md) |

