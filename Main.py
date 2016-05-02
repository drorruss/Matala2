import os
import Create_Table as r
import Parser_Csv as csv
import Parser__kml as kml

i=r.read_dir ("C:\\Users\\wim7\\Desktop\\exam")
print (i)
for n in range (1,i+1):
    csv.create_csv(n)
    kml.create_kml(n)
    