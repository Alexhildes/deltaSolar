# Author: Alex Hildebrand
# Date: 28/11/2022
# RS485 over IP sniffer
# Delta Solivia 2.5 G3 Inverter
# Using Influxdb 2.0 on Docker Image


import serial
import time
import sys
import json
import influxdb_client
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

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

# InfluxDB objects
bucket = "Nollamara"
org = "alex"
token = "YB1zNcwJAMxSSavEQTO-e91vFJ_AMVI9HL19yhAS80KYC0kigHiTK2X_hiTJ844_8NwGR6BxzvWF1CLkoV5_fQ=="
url = "http://192.168.1.210:8086"

# Influxdb client
client = influxdb_client.InfluxDBClient(url, token, org)

write_api = client.write_api(write_options=SYNCHRONOUS)

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
        write_api.write(bucket, org, data)
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
