import csv
import os
from datetime import date, datetime, timedelta

fields = ['Date']
for i in range(24):
	for j in range(4):
		hour = f"0{i}" if i<10 else f"{i}"
		mins = f"{j*15}" if j!=0 else f"0{j}"
		timeslot = f"{hour}:{mins}"
		fields.append(timeslot)
#print(fields)

# name of csv file
filename = "data.csv"

def initialize():
        with open(filename, 'w', newline = '\n') as csvfile:
                csvwriter = csv.writer(csvfile)  # creating a csv writer object		
                csvwriter.writerow(fields)
                print('New file "data.csv" created!')

def csv_append(lst):
        with open(filename, 'a', newline = '\n') as csvfile:
                csvwriter = csv.writer(csvfile)  # creating a csv writer object		
                csvwriter.writerow(lst)
                print('1 row added to data.csv')

def getrows():
        rows=[]
        with open(filename) as csvfile:
                csvreader = csv.reader(csvfile)  # creating a csv reader object	                                                                                                                       	
                for x in csvreader:
                        rows.append(x)
        return rows[1:]	

def csv_isExist(date):
	with open(filename, 'r') as csvfile:
		rows = getrows()
		isExist = False
		for row in rows:
			if row[0]==date:
				isExist =True
				break
		return isExist		

def replace_row(date, row_list):
        with open('data.csv') as inf, open('data_temp.csv', 'w', newline='\n') as outf:
                reader = csv.reader(inf)
                writer = csv.writer(outf)
                for line in reader:
                        #print(line)
                        if line[0] == str(date):
                                writer.writerow(row_list)
                        else:
                                writer.writerow(line)

        os.remove('data.csv')
        os.rename('data_temp.csv', 'data.csv')	
        print('1 row replaced')	

def get_range(start_date, end_date):
        range_in_focus = []

        rows = getrows()
        for row in rows:
                date = datetime.strptime(row[0], '%Y-%m-%d').date()
                if start_date<=date<=end_date:
                        range_in_focus.append(row)
        return range_in_focus                