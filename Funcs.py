import os.path
import sqlite3


sum=0
def read_directory(str):
    j=0
    global sum
    if os.path.isdir(str):
       for file in os.listdir(str):
           if ".nmea" in file:
               j=j+1
               read_file(str+"\\"+file,j)
               sum = j
    return j




def read_file(str1,i):
    with open (str1,'r')as op:
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('drop table if exists nmea' + str(i))
        c.execute('CREATE TABLE IF NOT EXISTS summary(startDate text,endDate text,startTime text, endTime text,maxSpeed text,minSpeed text)')
        c.execute('''CREATE TABLE nmea''' + str(i) + '''
                (time text, latitude text,north text, longtitude text,
                east text,quality text, nos text, hdop text, altitude text,
                hog text,speed text,date text)''')
        list=op.readlines()
        ind=0

        while ind<len(list)-1:             # Go over all the lines in the current file
            ind1 = find_GA(list,ind)     # Finding the next GPGGA line
            if (ind1==-1):                 # Checking if the GPGGA line is correct
                break
            line1 = checkLine(list[ind1])  # Fix line
            ind = ind1+1
            ind2 = findMC(list,ind)      # Finding the next GPRMC line
            if (ind2 == -1):               # Checking if the GPRMC line is correct
                break
            line2 = checkLine(list[ind2])  # Fix line
            ind=ind2+1
            load_DB(line1,line2,i)           # Enter the lines into the database
       # startTime=c.execute('SELECT MIN(time) FROM summary')
       # print(startTime,"\n")
        conn.close()
    return 1





def checkLine(line):                         # fix the line to start with '$'
    if (line[0] != '$'):
        k = 0
        while line[k] != '$':
            k = k + 1
        fix_line = line[k:]
        return fix_line
    return line




def find_GA(list,ind):
    while "GPGGA" not in list[ind] and ind<len(list)-2:
        ind=ind+1
    if ind >= len(list) - 1:
        return -1
    str=list[ind].split(",")
    if (str[1]==''):
        return find_GA(list,ind+1)

    return ind




def findMC(list,ind):
    while "GPRMC" not in list[ind] and ind<len(list)-2:
        ind=ind+1
    if ind>=len(list)-1:
        return -1
    str=list[ind].split(",")
    if (str[1]==''):
        return find_GA(list,ind+1)
    return ind





def load_DB(str1,str2,i):
    list1=str1.split(",")
    list2=str2.split(",")
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    # Insert a row of data
    c.execute("INSERT INTO nmea"+str(i)+" VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(list1[1], list1[2], list1[3], list1[4],list1[5], list1[6],list1[7], list1[8], list1[9], list1[10],list2[7],list2[9]))
    conn.commit()
    conn.close()




def dropAll():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    tables = list(c.execute("select name from sqlite_master where type is 'table'"))
    c.executescript(';'.join(["drop table if exists %s" % i for i in tables]))
    
    
    