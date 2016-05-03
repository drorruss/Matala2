import os
import Funcs as f
import Parser_Csv as csv
import Parser__kml as kml

i=f.read_directory ("C:\\Users\\Dror\\Desktop\\Benchmark")
print (i)
for n in range (1,i+1):
    csv.create_csv(n)
    kml.create_kml(n)
    