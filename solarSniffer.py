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
                "Address" : "02 05 01 02 10 08 20 3E 03",
                "Unit" : "Volts",
                "Type" : "WholeNumber",
                        },

            "CurrentAC" : {
                "Address" : "02 05 01 02 10 07 20 3E 03",
                "Unit" : "Amps",
                "Type" : "Decimal",
                        }

            }

ser=serial.serial_for_url("socket://192.168.1.212:8899/logging=debug",19200)
ser.flush()

while True:
	try:
		#Request
		ser.write(bytes.fromhex("02 05 01 02 10 07 20 3E 03"))

		#Response
		data = ser.read(11).hex()
		current = data[12:16]
		print(data)
		print(len(data))
		print(current)
		print(int(current,16)/10)
		
		time.sleep(5)

 
	except KeyboardInterrupt:
        	print("Exiting")
        	sys.exit(0)


	except Exception as e:
		print("Received Exception!")
		print(e)
		time.sleep(10)
