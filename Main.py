import os
import create_table as m
import nmea__csv as csv
import nmea__kml as kml

i=m.read_dir("C:\\Users\\Dror\\Desktop\\Benchmark - Copy")
print (i)
for x in range (1,i+1):
    csv.create_csv(x)
    kml.create_kml(x)
    