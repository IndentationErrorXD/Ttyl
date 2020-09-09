import csv
import os

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

def getrows(csvreader):
	rows=[]
	for x in csvreader:
		rows.append(x)
	return rows	

def csv_isEmpty(date):
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		rows = getrows(csvreader)
		isEmpty = True
		for row in rows:
			if row[0]==date:
				isEmpty = False
		return isEmpty		

def replace_row(date, row_list):
	with open('data.csv') as inf, open('data_temp.csv', 'w', newline='\n') as outf:
		reader = csv.reader(inf)
		writer = csv.writer(outf)
		for line in reader:
			if line[0] == date:
				writer.writerow(row_list)
			else:
				writer.writerow(line)

	os.remove('data.csv')
	os.rename('data_temp.csv', 'data.csv')	
	print('1 row replaced')	

