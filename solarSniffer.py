# Author: Alex Hildebrand
# Date: 28/03/2022
# RS485 over IP sniffer
# Delta Solivia 2.5 G3 Inverter

import serial
import time
import sys
from influxdb import InfluxDBClient
import json


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

# Create the InfluxDB client object
client = InfluxDBClient(host='localhost', port=8086, database='db_Nolla')

def write_data(voltageAC, currentAC, powerAC, measurement="DeltaSolar", device="Serial Gateway"):

     # Create the JSON data structure
        iso = time.ctime()
        data = [{
            "measurement": measurement,
                "tags": {
                    "device" : device,
                },
                "fields": {
                    "VoltageAC" : voltageAC,
                    "CurrentAC" : currentAC,
                    "PowerAC" : powerAC,
		}
            }]

        # Send the JSON data to InfluxDB
        client.write_points(data)
        print(iso + ' - Data Sent to InfluxDB')


# Blank responses dict
r = {}

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

				r[k]=value

			else:
				print("No valid response received, moving to next")
				v=0
				#r.update[k]=v

			time.sleep(1)
		r["PowerAC"] = r["VoltageAC"]*r["CurrentAC"]
		print(r)

		write_data(r["VoltageAC"],r["CurrentAC"],r["PowerAC"])

		time.sleep(30)

	except KeyboardInterrupt:
        	print("Exiting")
        	sys.exit(0)


	except Exception as e:
		print("Received Exception!")
		print(e)
		time.sleep(10)
