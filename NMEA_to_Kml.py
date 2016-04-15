import os.path
import sqlite3
import time

def format_time(value):
    hour = value[:2]
    minute = value[2:4]
    second = value[4:6]
    timeval = hour + ":" + minute + ":" + second + "Z"
    return timeval
def format_date(value):
    day = value[:2]
    month = value[2:4]
    year = value[4:6]
    dateval = "20"+year+"-"+month+"-"+day+"T"
    return dateval
def knots_to_kph(value):
    return   str("%.2f" %(float(value)*1.85200)) +" km/h"

def create_kml(i):
    my_category = 0
    skip=5
    database = sqlite3.connect('example.db')
    pois = database.execute("SELECT * FROM nmea" + str(i))
    file = 'file' + str(i) + '.kml'
    FILE = open(file, 'w')
    FILE.truncate(0)
    FILE.write('<?xml version="1.0" encoding="iso-8859-1"?>\n')
    FILE.write('<kml xmlns="http://earth.google.com/kml/2.0">\n')
    FILE.write('    <Document>\n')
    FILE.write('     <Folder>\n')
    FILE.write('     <name>Point Features</name>\n')
    FILE.write('     <description>Point Features</description>\n\n')
    j=0
    for poi in pois:
        if j%skip==0:
            print('%s : %s, %s' % (poi, poi[2], poi[1],))
            FILE.write('<Placemark>\n')
            FILE.write('    <TimeStamp>\n')
            FILE.write('     <when>%s%s</when>\n' % (format_date(poi[11]),format_time(poi[0])))
            FILE.write('    </TimeStamp>\n')
            lat = float(poi[1][:2]) + (float(poi[1][2:]) / 60)
            lon = float(poi[3][:3]) + (float(poi[3][3:]) / 60)
            FILE.write('    <description><![CDATA[Lat: %s <br> Lon: %s<br> Speed: %s <br>]]></description>\n' % (lat, lon,knots_to_kph(poi[10])))
            FILE.write('    <Point>\n')

            FILE.write('        <coordinates>%s,%s,%s</coordinates>\n' % (str(lon), str(lat), poi[8]))
            FILE.write('    </Point>\n')
            FILE.write('</Placemark>\n')
            j=j+1
        else:
            j=j+1
    FILE.write('        </Folder>\n')
    FILE.write('    </Document>\n')
    FILE.write('</kml>\n')
    FILE.close()
    database.close()