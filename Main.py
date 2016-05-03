import os
import Funcs as f
import Parser_Csv as csv
import Parser__kml as kml

i=f.read_dir ("C:\\Users\\Dror\\Desktop\\exam")
print (i)
for n in range (1,i+1):
    csv.create_csv(n)
    kml.create_kml(n)
    