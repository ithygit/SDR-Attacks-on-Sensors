# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# Refer to https://mavlink.io/en/mavgen_python/ for the MAVLink lib
# Refer to https://mavlink.io/en/messages/common.html for MAVLink messages

#import time
import csv
from pymavlink import mavutil
import keyboard
import matplotlib.pyplot as plt

# Start a connection listening to a UDP port
the_connection = mavutil.mavlink_connection('udpin:192.168.99.2:14550')

# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_system))

# Once connected, use 'the_connection' to get and send messages

csv_filename = 'drone_status.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    field = ['time', 'fix_type', 'EKF_status','lat', 'lon', 'alt', 'vel_acc', 'h_acc', 'v_acc']
    csvwriter.writerow(field);
    print(field)
    
    lat_list = []
    lon_list = []

    while not keyboard.is_pressed('c'):
        the_connection.wait_heartbeat()
        time_usec = the_connection.messages['GPS_RAW_INT'].time_usec # time since system boot in us
        fix_type = the_connection.messages['GPS_RAW_INT'].fix_type # 1: No fix, 3: 3D fix
        ekf_status = the_connection.messages['EKF_STATUS_REPORT'].flags
        lat = the_connection.messages['GPS_RAW_INT'].lat # degE7
        lon = the_connection.messages['GPS_RAW_INT'].lon
        alt = the_connection.messages['GPS_RAW_INT'].alt # mm
        vel_acc = the_connection.messages['GPS_RAW_INT'].vel_acc # Speed uncertainty in mm
        h_acc = the_connection.messages['GPS_RAW_INT'].h_acc # Position uncertainty in mm
        v_acc = the_connection.messages['GPS_RAW_INT'].v_acc # Altitude uncertainty in mm
        
        time_s = time_usec / 1000000
        lat_deg = lat / 10000000
        lon_deg = lon / 10000000
        alt_deg = alt / 10000000
        vel_acc_m = vel_acc / 1000
        h_acc_m = h_acc / 1000
        v_acc_m = v_acc / 1000
        
        lat_list.append(lat_deg)
        lon_list.append(lon_deg)
        
        row = [time_s, fix_type, ekf_status, lat_deg, lon_deg, alt_deg, vel_acc_m, h_acc_m, v_acc_m]
        csvwriter.writerow(row);
        print(row)
    
    # time.sleep(0.25)
    fig = plt.figure(figsize=(16,9))
    plt.title('Drone trajectory')
    plt.xlabel('Longitude(deg)')
    plt.ylabel('Latitude(deg)')
    #plt.xticks(np.arange(50, 160, 10.0))
    plt.grid(b=True, which='both')
    plt.scatter(x=lon_list, y=lat_list);
    plt.plot(lon_list[0], lat_list[0], 'gs', markersize = 12);
    plt.plot(lon_list[-1], lat_list[-1], 'r^', markersize = 12);
    