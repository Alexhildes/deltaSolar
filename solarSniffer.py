# Author: Alex Hildebrand
# Date: 28/03/2022
# RS485 over IP sniffer
# Delta Solivia 2.5 G3 Inverter

import serial
import time
import sys

#Gateway Configuration
gateway =   {
            "ipaddress" : "192.168.1.212",
            "port" : "8899"
            }

#Addresses
registers = {
            "VoltageAC" : {
                "Address" : "02 05 01 02 10 08 60 3A 03",
                "Unit" : "Volts",
                "Divisor" : 1,
                        },

            "CurrentAC" : {
                "Address" : "02 05 01 02 10 07 20 3E 03",
                "Unit" : "Amps",
                "Divisor" : 10,
                        }

            }

#Timeout
timeout = 5

ser=serial.serial_for_url("socket://192.168.1.212:8899/logging=debug",19200,timeout=timeout)
ser.flush()
print("Flushed serial port")

while True:
	try:

		for k,v in registers.items():
			#Request
			print("Requesting " + k)
			ser.write(bytes.fromhex(v["Address"]))

			#Response
			response = ser.read(11).hex()
			if len(response) == 22:
				value = response[12:16]
				value = int(value,16)/v["Divisor"]
				print("Request received for " + k)
				print(value)
				print(v["Unit"])

			else:
				print("No valid response received, moving to next")

			time.sleep(1)

		time.sleep(5)

	except KeyboardInterrupt:
        	print("Exiting")
        	sys.exit(0)


	except Exception as e:
		print("Received Exception!")
		print(e)
		time.sleep(10)
