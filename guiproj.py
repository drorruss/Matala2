from tkinter import *
import os.path
import sqlite3
import csv
from datetime import datetime
import math
import os
import time


# NMEA To DB #
def load():
    conn = sqlite3.connect('nmea_to_db.db')
    c = conn.cursor()
    tables = list(c.execute("select name from sqlite_master where type is 'table'"))
    c.executescript(';'.join(["drop table if exists %s" % i for i in tables]))
        
    INPUT = 'NMEAFiles'
    if os.path.isdir(INPUT):
        l = os.listdir(INPUT)
        for k in range(len(l)):
            nmea(INPUT + "\\"+l[k],l[k])

def getRMCdata(row):
    warning = row[2]
    if warning == 'V':
        return
    time = row[1]
    latitude = row[3]
    lat_direction = row[4]
    longitude = row[5]
    lon_direction = row[6]
    speed = row[7]
    date =  row[9]
    listRMC = [speed,date,time,latitude,lat_direction,longitude,lon_direction]
    return listRMC

def nmea(INPUT,TableName):
    conn = sqlite3.connect('nmea_to_db.db')
    c = conn.cursor()
    l = str(TableName)
    listName = l.split('.')
    print(listName)

    
    c.execute('drop table if exists ' + str(listName[0]) )
    c.execute('''CREATE TABLE '''+ str(listName[0]) + '''
                         (time text ,latitude text,latitude_direction text,
                         longitude text,longitude_direction text,fix text,numOfSat, horizontal_dilution text,
                          altitude text,direct_of_altitude text,altitude_location text ,speed float ,date text)''')

    with open(INPUT, 'r') as input_file:
        reader = csv.reader(input_file)
        #flag will tell us if the GPGGA is good if yes continue to the GPRMC
        flag = 0
        # create a csv reader object from the input file (nmea files are basically csv)
        for row in reader:
            # skip all lines that do not start with $GPGGA
            if not row:
                continue
            elif row[2] is None:  
                continue
            elif row[2] == "":  
                continue
            elif "GGA" in row[0]  :
                time = row[1]
                latitude = row[2]
                lat_direction = row[3]
                longitude = row[4]
                lon_direction = row[5]
                fix = row[6]
                numOfSat = row[7]
                horizontal = row[8]
                altitude = row[9]
                direct_altitude = row[10]
                altitude_location = row[11]
                flag = 1
                c.execute("INSERT INTO "+str(listName[0])+" VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(time,
                                                                               latitude,
                                                                                lat_direction,
                                                                               longitude,
                                                                                lon_direction,
                                                                                fix,
                                                                                 numOfSat ,              
                                                                               horizontal,
                                                                                altitude,
                                                                               direct_altitude,
                                                                               altitude_location,' ',' ' ))

            elif "RMC" in row[0]:
                listRMC = getRMCdata(row)
                if( listRMC!= None):
                    c.execute("INSERT INTO " + str(listName[0]) + " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            (listRMC[2],listRMC[3],listRMC[4],listRMC[5],listRMC[6],' ',' ',' ',' ',' ',' ',listRMC[0],listRMC[1] ))
                    # Save (commit) the changes
                conn.commit()
                flag=0
            else:
                continue
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.commit()
    conn.close()

        # To CSV #

def toCSV():
    conn = sqlite3.connect("nmea_to_db.db") #open db
    cursor = conn.cursor() #cursor to the db
    INPUT = 'NMEAFiles'
    if os.path.isdir(INPUT):
        l = os.listdir(INPUT)
        for k in range(len(l)):
            spl = str(l[k])
            listName = spl.split('.')
            cursor.execute('SELECT * FROM '+str(listName[0]) )
            print ("[ '" + str(listName[0])+"' , CSV FILE ]")
            with open("CSV\\"+listName[0]+".csv", "wb") as csv_file: #writing to csv
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([i[0] for i in cursor.description]) # write headers
                csv_writer.writerows(cursor)

        # To KML #

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
    if value is None :# if value == None:
        return ' '
    elif value == "":  # if row[2].len() == 0:
        return ' '
    elif value == " ":  # if row[2].len() == 0:
        return ' '
    else :
        return   str("%.2f" %(float(value)*1.85200)) +" km/h"

    
def kml():
    my_category = 0
    skip=5
    database = sqlite3.connect('nmea_to_db.db')
    INPUT = 'NMEAFiles'
    if os.path.isdir(INPUT):
        l = os.listdir(INPUT)
        for k in range(len(l)):
            spl = str(l[k])
            listName = spl.split('.')
            print("[ '"+listName[0] + "' , KML FILE ]")
            pois = database.execute("SELECT * FROM "+str(listName[0]) )
            file = "KML\\"+str(listName[0])+".kml"
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
                    FILE.write('<Placemark>\n')
                    FILE.write('    <TimeStamp>\n')
                    FILE.write('     <when>%s%s</when>\n' % (format_date(poi[12]),format_time(poi[0])))
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
    


        #MyQuerys#

def myquery(q):
    con = sqlite3.connect("nmea_to_db.db")
    con.isolation_level = None
    cur = con.cursor()

    buffer = ""

    print ("Enter your SQL commands to execute in sqlite3.")
    print ("Enter a blank line to exit.")

    while True:
        line = q
        if line == "":
            break
        buffer += line
        if sqlite3.complete_statement(buffer):
            try:
                buffer = buffer.strip()
                cur.execute(buffer)

                if buffer.lstrip().upper().startswith("SELECT"):
                    root = Tk()
                    root.title("Query ''Select'' result")
                    root.geometry("750x550")
                    app = Frame(root)
                    app.grid()
                    S = Scrollbar(root)
                    T = Text(app, height=100, width=100)
                    S.pack(side=RIGHT, fill=Y)
                    T.pack(side=LEFT, fill=Y)
                    S.config(command=T.yview)
                    T.config(yscrollcommand=S.set)
                    for row in cur.execute(buffer):
                        T.insert(INSERT,row)
                        T.insert(INSERT, "\n")
                    T.pack()    
                    break
            except sqlite3.Error as e:
                print ("An error occurred:", e.args[0])
                break
            buffer = ""

    con.close()
    
        # Google Erth #

def showGoogleEarth():
    if os.path.isdir('KML'):
        l = os.listdir('KML')
        for k in range(len(l)):
            l2 = str(l[k])
            os.startfile('KML\\'+l2)
            time.sleep(5)

        # Main #

def querytxt():
    get = query.get()
    get1 = query1.get()
    comm = "select "+get+" from "+get1+";"
    
    querys.myquery(comm)
    return

root = Tk()
root.title("NMEA TO CSV PROGRAM")
root.geometry("310x250")
app = Frame(root)
app.grid()
query = StringVar()
query1 = StringVar()

NmeaRunButton = Button(app , text = "nmea 2 DB" , command = load)
NmeaRunButton.pack()

ConvertToCSVbutton = Button(app , text = "2 CSV" , command = toCSV)
ConvertToCSVbutton.pack()

ConvertToKMLbutton = Button(app ,text = "2 KML"  , command = kml)
ConvertToKMLbutton.pack()

GoogleEbutton = Button(app , text = "See Google Maps"  , command =  showGoogleEarth)
GoogleEbutton.pack()

L1 = Label(app, text="Enter Query for Example :data/time..")
L1.pack()

Question = Entry(app,width = 50, textvariable = query)
Question.pack()

L2 = Label(app, text="Enter NMEA File names ")
L2.pack()

Question1 = Entry(app,width = 30, textvariable = query1)
Question1.pack()

EnterQuery = Button(app , text = "Enter", command = querytxt)
EnterQuery.pack()

mainloop()