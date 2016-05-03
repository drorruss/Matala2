import csv
import sqlite3

def create_csv(j):
    conn = sqlite3.connect('example.db')
    conn.text_factory = str 
    cur = conn.cursor()
    data = cur.execute("SELECT * FROM nmea"+str(j))
    with open('file'+str(j)+'.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'latitude', 'north\south','longtitude','east\west','quality','nos','hdop','altitude','hog','speed','date'])
        writer.writerows(data)