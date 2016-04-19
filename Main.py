import os
import create_table as m
import nmea__csv as c
import nmea__kml as kml

i=m.read_dir("C:\\Users\\Dror\\Desktop\\Benchmark - Copy")
print (i)
for x in range (1,i+1):
    c.create_csv(x)
    kml.create_kml(x)
    
s=input("Press 1 to enter folder, press 2 to enter a file:\n")
while s is not "1" and s is not "2":
    s = input("Wrong input, please Press 1 to enter folder, press 2 to enter a file:\n")
if s is "1":
    path=input("Please enter a folder path:\n")
    if os.path.isdir(path):
        counter = m.read_dir(path)
    else:
        print("Not a folder path.")
else:
    path = input("Please enter a file path:\n")
    if os.path.isfile(path):
        counter = m.read_file(path)
    else:
        print("Not a file path.")

print(s)