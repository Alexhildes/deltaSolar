# Author: Alex Hildebrand
# Date: 28/03/2022
# RS485 over IP sniffer
# Delta Solivia 2.5 G3 Inverter

from cgi import test
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

test
