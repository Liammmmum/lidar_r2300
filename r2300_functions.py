import time
import json
import requests
import array as arr
import math
import numpy as np

# define function to create_file
def save_ip(sensor_ip_address, pc_ip_address):
    file = open('network.dat', 'w')
    file.write(str(sensor_ip_address) + '\n' + str(pc_ip_address) + '\n')
    file.close()
    print('network setup:' + '\n' + 'sensor_ip_address:'+ sensor_ip_address + '\n' + 'pc_ip_address:' + pc_ip_address + '\n')

def send_request(url):
    try:
        r = requests.get(url, timeout=3)
        print(r.text)
    except:
        print ('error: no connection')
        return

def request_handle(url):
    try:
        r = requests.get(url, timeout=3)
        data = r.json()
        handle =data['handle']
        file = open('handle.dat', 'w')
        file.write(handle)
        file.close()
        print(r.text)
    except:
        print ('error: no connection')
        return

def read_ip():
    file = open('network.dat', 'r')
    content = file.read().splitlines()
    file.close()
    # print('network setup:' + '\n' + 'sensor_ip_address:'+ content[0] + '\n' + 'pc_ip_address:' + content[1] + '\n')
    return (content)

def check_ip():
    print('network setup:' + '\n' + 'sensor_ip_address:'+ read_ip()[0] + '\n' + 'pc_ip_address:' + read_ip()[1] + '\n')

def read_handle():
    file = open('Handle.dat', 'r')
    content = file.read()
    file.close()
    return (content)

def twos_complement_to_decimal(binary_str):
    n = len(binary_str)
    
    # Check if the number is negative
    if binary_str[0] == '1':
        # Invert all bits
        inverted_bits = ''.join('1' if bit == '0' else '0' for bit in binary_str)
        # Convert inverted binary to decimal and add 1
        decimal = int(inverted_bits, 2) + 1
        # Make it negative
        decimal = -decimal
    else:
        # Convert directly to decimal
        decimal = int(binary_str, 2)

    return decimal

import socket

def socket_connect(pc_ip_address, status):

    HOST = pc_ip_address
    PORT = 6464
    global stop_function
    Status = status
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)
    try: 
        s.bind((HOST, PORT))
        print('server start at: %s:%s' % (HOST, PORT))
        while True:  
                indata, adder = s.recvfrom(65536)        
                magic = hex(indata[1]) +','+ hex(indata[0])
                packet_type = chr(indata[2]) + chr(indata[3])
                packet_size = indata[7]*(256**3)+indata[6]*(256**2)+indata[5]*256+indata[4]
                header_size = indata[9]*256+indata[8]
                scan_number = indata[11]*256+indata[10]
                packet_number = indata[13] * 256 + indata[12]
                layer_index = indata[15] * 256 + indata[14]
                layer_inclination = (twos_complement_to_decimal(bin(indata[19]*(256**3)+indata[18]*(256**2)+indata[17]*256+indata[16])[2:].zfill(32))/10000)
                timestamp_raw = (indata[27]*(256**7)+indata[26]*(256**6)+indata[25]*(256**5)+indata[24]*(256**4)+indata[23]*(256**3)+indata[22]*(256**2)+indata[21]*256+indata[20])
                status_flags = indata[39]*(256**3)+indata[38]*(256**2)+indata[37]*256+indata[36]
                scan_frequency =  (indata[43] * (256**3)+indata[42] * (256**2)+ indata[41] * (256) + indata[40])/1000
                num_points_scan = indata[45] * 256 + indata[44]
                num_points_packet = indata[47] * 256 + indata[46]
                first_index = indata[49] * 256 + indata[48]
                first_angle = (twos_complement_to_decimal(bin(indata[53]*(256**3)+indata[52]*(256**2)+indata[51]*256+indata[50])[2:].zfill(32))/10000)
                angular_increment = ((indata[57]*(256**3)+indata[56]*(256**2)+indata[55]*256+indata[54])/10000)
                header_padding = indata[83] * 256 + indata[82]
                scan_point_data_bin = []
                scan_point_data = []
                distance_array = []
                amplitude_array = []
                
                for i in range(header_size,packet_size,4):
                    # scan_point_data_bin.append([indata[i+3], indata[i+2], indata[i+1], indata[i]])
                    # scan_point_data.append([hex(indata[i+3]), hex(indata[i+2]), hex(indata[i+1]), hex(indata[i])])
                    distance_array.append(((indata[i+3]*(256**3)+indata[i+2]*(256**2)+indata[i+1]*256+indata[i])& 1048575))
                    amplitude_array.append((((indata[i+3]*(256**3)+indata[i+2]*(256**2)+indata[i+1]*256+indata[i]))>>20))
                print('recvfrom ' + str(adder))
                print('magic:' + magic)
                print('packet_type:' + packet_type)
                print('packet_size:' + str(packet_size)) 
                print('header_size:' + str(header_size)) 
                print('scan_number:' + str(scan_number)) 
                print('packet_number:' + str(packet_number)) 
                print('layer_index:' + str(layer_index)) 
                print('layer_inclination:' + str(layer_inclination))
                print('timestamp_raw:' + str(timestamp_raw))
                print('status_flags:' + str(status_flags))
                print('scan_frequency:' + str(scan_frequency))
                print('num_points_scan:' + str(num_points_scan))
                print('num_points_packet:' + str(num_points_packet))
                print('first_index:' + str(first_index))
                print('first_angle:' + str(first_angle))
                print('angular_increment:' + str(angular_increment))
                print('header_padding:' + str(header_padding))
                print('distance:' + str(distance_array))
                # print(len(distance_array))
                print('amplitude:' + str(amplitude_array))
                # print(len(amplitude_array))

    except:           
            s.close()
            print ('socket closed')

# http commands
def http_commands (command):
    url = 'http://'+ read_ip()[0] + '/cmd/' + command
    # url_get_protocol_info = 'http://'+ read_ip()[0] + '/cmd/get_protocol_info'
    # url_get_parameter = 'http://'+ read_ip()[0] + '/cmd/get_parameter?'
    # url_request_handle = 'http://'+ read_ip()[0] + '/cmd/request_handle_udp?address='+ read_ip()[1] + '&port=6464&packet_type=C1'
    # url_start_scanoutput = 'http://'+ read_ip()[0] + '/cmd/start_scanoutput?handle='+ read_handle()
    # url_stop_scanoutput = 'http://'+ read_ip()[0] + '/cmd/stop_scanoutput?handle='+ read_handle()
    # url_release_handle = 'http://'+ read_ip()[0] + '/cmd/release_handle?handle='+ read_handle()
    return url

print('current network setup:' + '\n' + 'sensor_ip_address:'+ read_ip()[0] + '\n' + 'pc_ip_address:' + read_ip()[1] + '\n')


    
