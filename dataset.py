# create 15000 numbers with 1-9 as first digit

import random
import csv



# create 15000 numbers with 1-9 as first digit and save to csv file 
with open('data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(15000):
        writer.writerow([str(random.randint(1, 9)) + str(random.randint(0, 999999999))])
