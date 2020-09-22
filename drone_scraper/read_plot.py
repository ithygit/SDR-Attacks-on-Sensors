# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:28:29 2020

@author: jianqiu
"""

import pandas as pd
import matplotlib.pyplot as plt
import utm

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

# Plot the drone GPS trajectory
# df = pd.read_csv ('drone_status1.csv')
df = pd.read_csv ('drone_status2.csv')

# fig, ax = plt.subplots()
fig = plt.figure(constrained_layout=True)
plt.title('Drone trajectory')
plt.xlabel('X (meter)')
plt.ylabel('Y (meter)')
plt.grid(b=True, which='both')
# plt.ticklabel_format(useOffset=False)
plt.ticklabel_format(style='plain')
plt.axis('equal')

# Plot GPS points
meter1_x, meter1_y, _, _ = utm.from_latlon(df['lat'].values, df['lon'].values)
scatter1 = plt.scatter(x=meter1_x, y=meter1_y, c=df['fix_type'], cmap='Paired', zorder=2)
start_x = meter1_x[0]
start_y = meter1_y[0]
end_x = meter1_x[-1]
end_y = meter1_y[-1]
easting, northing, zone_number, zone_letter = utm.from_latlon(df['lat'].values[0], df['lon'].values[0])
# Plot arrows
# plt.quiver(x[:-1], y[:-1], x[1:]-x[:-1], y[1:]-y[:-1], scale_units='xy', angles='xy', scale=1, width=0.001, zorder=3, color='blue')
plt.quiver(meter1_x[:-1], meter1_y[:-1], meter1_x[1:]-meter1_x[:-1], meter1_y[1:]-meter1_y[:-1], scale_units='xy', angles='xy', scale=1, width=0.001, zorder=3, color='blue')
# Starting point
starting_point, = plt.plot(meter1_x[0], meter1_y[0], 'gs', zorder=1, markersize=10)
 # End point
end_point, = plt.plot(meter1_x[-1], meter1_y[-1], 'r^', zorder=1, markersize=10)

# Plot the original spoofing trajectory
df2 = pd.read_csv ('lowercampus.txt', header=None)
lat2 = (df2[2]//100 + df2[2]%100/60) * ((df2[3]=="N") * 2 - 1)
lon2 = (df2[4]//100 + df2[4]%100/60) * ((df2[5]=="E") * 2 - 1)
meter2_x, meter2_y, _, _ = utm.from_latlon(lat2.values, lon2.values)
scatter2 = plt.scatter(x=meter2_x, y=meter2_y, marker='*', s=10, zorder=3)
plt.plot(meter2_x[0], meter2_y[0], 'gs', zorder=1, markersize=10)
plt.plot(meter2_x[-1], meter2_y[-1], 'r^', zorder=1, markersize=10)

legend1 = plt.legend((starting_point, end_point, scatter2), ('Starting point', 'End point', 'Original trajectory'), loc = 'upper right')
classes = ['No fix', '3D fix']
plt.gca().add_artist(legend1)
legend2 = plt.legend(handles=scatter1.legend_elements()[0], labels=classes, title = 'Drone trajectory', loc = 'lower right')

# Secondary axes
ax = plt.gca()
secaxx = ax.secondary_xaxis('top', functions=(meter2lon, lon2meter))
secaxx.set_xlabel('Longitude(deg)')
secaxy = ax.secondary_yaxis('right', functions=(meter2lat, lat2meter))
secaxy.set_ylabel('Latitude(deg)')