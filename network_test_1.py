import ubinascii
import network
import urequests
import time
import socket
import neopixel
from machine import Pin
import esp
esp.osdebug(None)
import gc
gc.collect()
import led_ring
import log_function
import _thread

# send check
sending_failure = False

# Network credentials
ssid_list = ['Oliver Bootss iPhone 11 Pro Max','TP-Link_99E2','LTE-1931','Watson'] #'Watson'
password_list = ['RuneLite','15853172','12345678','vuvcth8txxmeisx'] #'vuvcth8txxmeisx'

#Passcode for website access:
web_passcode="a4a6d723-8ece-4c24-b662-0285cf9f1e50"
#user_id="c1ac11a9-dc44-46c9-a990-ee2ac711e9c6" # user 1
user_id="4a8e5bf7-b83d-4d90-9f0c-c3fab3c2ce6b" # user 2  
# send timer
send_timer = time.time()

def connect_to_wifi(ssid, password):
    #print('inside connect_to_wifi function')
    try:
        # For ESP to connect
        station = network.WLAN(network.STA_IF)
        station.active(True)
        station.connect(ssid, password)
        #print('ssid: ', ssid, 'pass: ', password) 
        station.mode(network.WLAN.N)
    except Exception as e:
        #print(f"Failed to connect to {ssid}")
        #print(f'error: {e}')
        #print('free memory: ',gc.mem_free())
        print('...')
        
        
def net_connect():
    for i in range(len(ssid_list)):
        #print('len of ssid_list:', len(ssid_list))
        #print('i: ', i)
        print(f'trying to connect to {ssid_list[i]}')
        connect_to_wifi(ssid_list[i], password_list[i])
        #print(f'network: {ssid_list[i]} index: {i} - password: {password_list[i]} index: {i}') 
        time.sleep(10)
        if network.WLAN(network.STA_IF).isconnected():
            print(f'Connected to {ssid_list[i]}')
            # led ring blinks blue when connected
            led_ring.led_connect()
            print('ip address: ',get_ip_address2()[0])
            # exit function if connected
            return

def net_disconnect():
    station = network.WLAN(network.STA_IF)
    station.active(False)
    print('disconnecting..')
    print('-----------------------------------------------------------------')


def mac_address():
    wlan_sta = network.WLAN(network.STA_IF)
    wlan_sta.active(True)
    wlan_mac = wlan_sta.config('mac')
    return ubinascii.hexlify(wlan_mac, ':').decode().upper()


def get_ip_address():
    return socket.gethostbyname((socket.gethostname()))


def get_ip_address2():
    wlan_sta = network.WLAN(network.STA_IF)
    #print(f'ip address: {wlan_sta.ifconfig()[0]}\nsubnet mask: {wlan_sta.ifconfig()[1]}\ndefault gateway: {wlan_sta.ifconfig()[2]}\ndns: {wlan_sta.ifconfig()[3]}')
    return wlan_sta.ifconfig()


def send_data(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect(("10.10.4.10", 3000))
    
    print('data: ', data)
    
    s.sendall(str.encode("\n".join([str(data[0]), str(data[1]), str(data[2]), str(data[3]), str(data[4]), str(data[5]),str(data[6])])))

    msg = s.recv(1024).decode("utf-8")
    print('msg: ', msg)
    print("values sent")


def init_data(length,activity):
    global sending_failure  # indsat global variabel, slet hvis alt fucker!
    try:
        new_data=[web_passcode, user_id, get_ip_address2()[0], mac_address(), time.time(), length, activity]
        send_data(new_data)
    except Exception as e:
        print(f'Exception: {e}')
        sending_failure = True  # indsat bool, slet hvis alt fucker!
        print(f'sending faliure fra init_data = {sending_failure}')
        log_function.write_data_to_file(new_data)
        #resend_data()
        # resend thread test
        #_thread.start_new_thread(resend_data,()) # indsat resend_data funktionen her, sleet hvis alt fucker
       
        
def net_work_test():
    # disconnect timer
    disconnect_timer = time.time()
    while True:
        current_time = time.time()
        # try to connect to availabe networks
        if not network.WLAN(network.STA_IF).isconnected():
            net_connect()
            print('-----------------------------------------------------------------')
        # disconnect from network every hour to get back on wifi in case it was down    
        if current_time - disconnect_timer > 3600:  #3600 is 1 hour  
            net_disconnect()
            disconnect_timer = time.time()


#  -----  forsøg på funktion der sender igen, hvis sending går galt.
'''
def last_line_of_txt():
    with open("log_of_data_not_sent.txt") as file:
        last_line = file.readlines()[-1]
        last_line = last_line.strip()[18:]
    return last_line

def init_data_resend():
    global sending_failure
    print('inde i init_data_resend funktionen')
    try:
        print('trying to resend')
        with open("log_of_data_not_sent.txt") as file:
            last_line = file.readlines()[-1]
            last_line = last_line.strip()[18:]
        new_data = last_line
        send_data(new_data)
        sending_failure = False
        print(f'sending faliure fra init_data_resend = {sending_failure}')
    except Exception as e:
        print(f'Exception: {e}')
        print('sending failed, retrying in 10 seconds')
        sleep(10)
        init_data_resend()
'''

def init_data_resend():
    global sending_failure
    print('Inside init_data_resend function')
    try:
        print('Trying to resend')
        with open("log_of_data_not_sent.txt") as file:
            last_line = file.readlines()[-1]
            last_line = last_line.strip()[19:-1]
        new_data = last_line
        print('Data to resend:', new_data)
        # replace "'" with nothing
        new_data = new_data.replace("'","")
        # strip spaces away
        new_data = new_data.strip()
        # split new_data string from txt file
        new_data = new_data.split(',')
        # make it a list
        #print('ip address: ', new_data_list[2])
        # replace new_data_list[2] with actual ip address
        new_data[2] = get_ip_address2()[0]
        #print('new_data_list = ', new_data_list)
        for i in range(len(new_data)-1):
            x = new_data[i].strip()
            new_data[i] = x
        # data is sent again
        send_data(new_data)
        sending_failure = False
        #print(f'Sending failure from init_data_resend = {sending_failure}')
    except Exception as e:
        print(f'Exception: {e}')
        print('Sending failed, retrying in 10 seconds')
        time.sleep(10)
        init_data_resend()
        
def resend_data():
    global sending_failure
    #print('Inside resend_data function')
    #print(f'Sending failure from resend data = {sending_failure}')
    while sending_failure:
        #print('inside while loop of resend_data')
        time.sleep(1)
        init_data_resend()