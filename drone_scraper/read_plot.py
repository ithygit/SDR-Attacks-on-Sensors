# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:28:29 2020

@author: jianqiu
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import utm
import numpy as np

def lat2meter(lat):
    try: 
        _, ret, _, _ = utm.from_latlon(lat, start_x)
        return ret
    except:
        return lat

def lon2meter(lon):
    try: 
        ret, _, _, _ = utm.from_latlon(start_y, lon)
        return ret
    except:
        return lon

def meter2lat(meter):
    try: 
        lat, _ = utm.to_latlon(easting, meter, zone_number, zone_letter)
        return lat
    except:
        return meter

def meter2lon(meter):
    try: 
        _, lon = utm.to_latlon(meter, northing, zone_number, zone_letter)
        return lon
    except:
        return meter

def plot_gps(gps_file, trajectory_file):
    df = pd.read_csv (gps_file)
    df['valid'] = [0] * df.shape[0]  # Add a column 'valid'
    # Generate valid indicators using a state machine
    # Set invalid the points before 3D fix and after spoofing signal transmission is done
    status = 0
    for index, row in df.iterrows():
        good_position = row['fix_type'] == 3 and row['vel_acc'] < 1 and row['h_acc'] < 10
        if status == 0:
            if not(good_position): # bad GPS signal
                status = 1
            df.at[index, 'valid'] = 0
        if status == 1:
            if good_position: # good GPS signal
                status = 2
            df.at[index, 'valid'] = 0
        if status == 2:
            if not(good_position): # bad GPS signal
                status = 3
            if row['vel'] >= 0.01:
                df.at[index, 'valid'] = 2   # Moving points
            else:
                df.at[index, 'valid'] = 1   # Static points
        if status == 3:
            df.at[index, 'valid'] = 0
    
    # fig, ax = plt.subplots()
    fig1 = plt.figure(constrained_layout=True)
    fig1.canvas.set_window_title(gps_file + ' - Drone Trajectory')
    plt.title('Drone Trajectory')
    plt.xlabel('X (meter)')
    plt.ylabel('Y (meter)')
    plt.grid(b=True, which='both')
    # plt.ticklabel_format(useOffset=False)
    plt.ticklabel_format(style='plain')
    plt.axis('equal')
    
    # Plot GPS points
    meter1_x, meter1_y, _, _ = utm.from_latlon(df['lat'].values, df['lon'].values)
    # Calculate the start and end points, and the utm parameters
    global start_x, start_y, end_x, end_y, easting, northing, zone_number, zone_letter
    # start_x = meter1_x[0]
    # start_y = meter1_y[0]
    # end_x = meter1_x[-1]
    # end_y = meter1_y[-1]
    easting, northing, zone_number, zone_letter = utm.from_latlon(df['lat'].values[0], df['lon'].values[0])
    # Plot the trajectory
    meter1_x = meter1_x[df['valid'] >= 1]
    meter1_y = meter1_y[df['valid'] >= 1]
    valid = df['valid'][df['valid'] >= 1]
    scatter1 = plt.scatter(x=meter1_x, y=meter1_y, c = valid, cmap='Blues', vmin=0, vmax=3, zorder=2, label = 'Positions from GPS_RAW_INT')
    # Plot arrows
    # plt.quiver(x[:-1], y[:-1], x[1:]-x[:-1], y[1:]-y[:-1], scale_units='xy', angles='xy', scale=1, width=0.001, zorder=3, color='blue')
    plt.quiver(meter1_x[:-1], meter1_y[:-1], meter1_x[1:]-meter1_x[:-1], meter1_y[1:]-meter1_y[:-1], scale_units='xy', angles='xy', scale=1, width=0.001, zorder=3, color='blue')
    # Start point
    start_point, = plt.plot(meter1_x[0], meter1_y[0], 'gs', zorder=1, markersize=10, label = 'Start point')
     # End point
    end_point, = plt.plot(meter1_x[-1], meter1_y[-1], 'r^', zorder=1, markersize=10, label = 'End point')
    
    # Plot the EKF drone trajectory
    EKF_position_x_list = []
    EKF_position_y_list = []
    new_x = meter1_x[0]
    new_y = meter1_y[0]
    for index, row in df.iterrows():
        # print(index, row['time'], row['global_vx'], row['global_vy'], row['global_vz'])
        # if index == 0: continue
        # if row['fix_type'] != 3 or row['vel_acc'] >= 1: continue # Discord points of no fix or low accuracy
        if row['valid'] == 0: continue 
        time = df.iloc[index]['time'] - df.iloc[index - 1]['time']
        new_x = new_x + time * row['global_vx']
        new_y = new_y + time * row['global_vy']
        EKF_position_x_list.append(new_x)
        EKF_position_y_list.append(new_y)
        # print(index, time, new_x, new_y)
    EKF_position_x = np.array(EKF_position_x_list)
    EKF_position_y = np.array(EKF_position_y_list)
    scatter2 = plt.scatter(x=EKF_position_x, y=EKF_position_y, c = valid, cmap='Greys', vmin=0, vmax=3, marker='o', zorder=3, label = 'Positions from velocity integral')
    plt.quiver(EKF_position_x[:-1], EKF_position_y[:-1], EKF_position_x[1:]-EKF_position_x[:-1], EKF_position_y[1:]-EKF_position_y[:-1], scale_units='xy', angles='xy', scale=1, width=0.001, zorder=3, color='blue')
    
    # Plot the original spoofing trajectory
    df2 = pd.read_csv (trajectory_file, header=None)
    lat2 = (df2[2]//100 + df2[2]%100/60) * ((df2[3]=="N") * 2 - 1)
    lon2 = (df2[4]//100 + df2[4]%100/60) * ((df2[5]=="E") * 2 - 1)
    meter2_x, meter2_y, _, _ = utm.from_latlon(lat2.values, lon2.values)
    scatter3 = plt.scatter(x=meter2_x, y=meter2_y, marker='*', color = 'purple', s=3, zorder=3, label = 'Original spoofing signal')
    plt.plot(meter2_x[0], meter2_y[0], 'gs', zorder=1, markersize=10)
    plt.plot(meter2_x[-1], meter2_y[-1], 'r^', zorder=1, markersize=10)
    
    # Plot the GPS points from global position
    global_meter1_x, global_meter1_y, _, _ = utm.from_latlon(df['global_lat'].values, df['global_lon'].values)
    global_meter1_x = global_meter1_x[df['valid'] >= 1]
    global_meter1_y = global_meter1_y[df['valid'] >= 1]
    scatter4 = plt.scatter(x=global_meter1_x, y=global_meter1_y, c = valid, cmap='Oranges', vmin=0, vmax=3, zorder=2, label = 'Positions from GLOBAL_POSITION_INT')    
    # Plot arrows    
    plt.quiver(global_meter1_x[:-1], global_meter1_y[:-1], global_meter1_x[1:]-global_meter1_x[:-1], global_meter1_y[1:]-global_meter1_y[:-1], scale_units='xy', angles='xy', scale=1, width=0.001, zorder=3, color='red')
    
    # Create the legend
    legend1 = plt.legend(handles=[start_point, end_point, scatter3], loc = 'upper right')
    # classes = ['No fix', '3D fix']
    plt.gca().add_artist(legend1)
    # legend2 = plt.legend(handles=scatter1.legend_elements()[0], labels=classes, title = 'Drone trajectory', loc = 'lower right')
    # legend2 = plt.legend(handles=[scatter1, scatter2, scatter3, scatter4], labels=classes, title = 'Drone trajectory', loc = 'lower right')
    # legend2 = plt.legend(*scatter2.legend_elements(num=1), title = 'Drone trajectory')
    handles = [scatter1.legend_elements()[0][1],
               scatter2.legend_elements()[0][1],
               scatter4.legend_elements()[0][1]]
    labels = ['Positions from GPS_RAW_INT',
              'Positions from velocity integral',
              'Positions from GLOBAL_POSITION_INT']
    legend2 = plt.legend(handles=handles, labels=labels, title = 'Drone trajectory', loc = 'lower right')


    # Secondary axes
    ax = plt.gca()
    secaxx = ax.secondary_xaxis('top', functions=(meter2lon, lon2meter))
    secaxx.set_xlabel('Longitude(deg)')
    secaxy = ax.secondary_yaxis('right', functions=(meter2lat, lat2meter))
    secaxy.set_ylabel('Latitude(deg)')
    
    
    # Plot the fix type and EKF status
    time = df['time'].values - df['time'].values[0]
    fig2, axs = plt.subplots(3)
    fig2.canvas.set_window_title(gps_file + ' - Drone Status')
    # fig2.tight_layout()
    axs[0].plot(time, df['fix_type'], '--', color='blue')
    axs[0].set_title('Fix type and EKF Status')
    # axs[0].set_xlabel('Time')
    axs[0].xaxis.set_minor_locator(MultipleLocator(10))
    axs[0].set_ylabel('Fix type', color='blue')
    axs[0].tick_params(axis='y', labelcolor='blue')
    axs[0].set_yticks([0, 1, 2, 3])
    axs[0].set_yticklabels(['0 - No GPS', '1 - No fix', '', '3 - 3D fix'])
    ax0b = axs[0].twinx()
    ax0b.plot(time, df['EKF_status'], '-', color='orange')
    ax0b.set_ylabel('EKF Status', color='orange')
    ax0b.tick_params(axis='y', labelcolor='orange')
    # axs[0].legend()
    # Plot accuracy
    axs[1].plot(time, df['h_acc'], label = 'Position Accuracy')
    axs[1].plot(time, df['vel_acc'], label = "Velocity Accuracy")
    axs[1].set_title('Position and Velocity Accuracy')
    axs[1].xaxis.set_minor_locator(MultipleLocator(10))
    axs[1].set_ylabel('(m)')
    axs[1].set_ylim(0,100)
    axs[1].legend()
    # Plot ground speed
    axs[2].plot(time, df['vel'], '-', label = 'Ground Speed from GPS_RAW_INT')
    # axs[2].plot(time, df['HUD_groundspeed'], '--', label = 'Ground Speed from HUD')
    # axs[2].plot(time, df['HUD_airspeed'], '-.', label = 'Air Speed from HUD')
    vx = df['global_vx'].values
    vy = df['global_vy'].values
    speed = (vx**2 + vy**2) ** .5
    axs[2].plot(time, speed, color='orange', label = 'Ground Speed from GLOBAL_POSITION_INT ')
    axs[2].set_title('GPS Ground Speed')
    axs[2].set_xlabel('Time')
    axs[2].xaxis.set_minor_locator(MultipleLocator(10))
    axs[2].set_ylabel('from GPS_RAW_INT (m/s)')
    axs[2].set_ylim(0,1)
    axs[2].legend(loc = 'upper left')
    ax2b = axs[2].twinx()
    ax2b.plot(time, df['global_alt'], ':', color='green', label = 'Altitude from GLOBAL_POSITION_INT ')
    ax2b.set_ylabel('from GLOBAL_POSITION_INT (m/s)', color='green')
    ax2b.tick_params(axis='y', labelcolor='green')
    # ax2b.set_ylim(0,6)
    ax2b.legend(loc = 'upper right')

# Plot the drone GPS trajectory
# plot_gps ('drone_status.csv', 'lowercampus.txt')
# plot_gps ('drone_status2.csv')
# plot_gps ('drone_status6.csv', 'holmes6.txt')
plot_gps ('drone_status15.csv', 'lowercampus15.txt')
