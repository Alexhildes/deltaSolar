# deltaSolar
RS485 over IP metric sniffer from a Delta Soliva 2.5

```In Python 3 byte objects are different to strings. The first thing that needs to be done is to convert the hex in to a byte object which then can be written on the serial port.

import serial
port = "/dev/ttyAMAO"
usart = serial.Serial (port,4800)
message_bytes = bytes.fromhex("0111050200013F0804")
usart.write(message_bytes)
```