from tkinter import *
from datetime import date
import file_handling as fh
import help_functions as hp
import os

#activity_data = [] #stores the color values of all timeslots/Button UPON SAVING

if os.path.exists('data.csv') == False:
	fh.initialize()

root = Tk()
root.title("Time Matrix")

grid_frame = LabelFrame(root, padx=10, pady=10)
grid_frame.pack()

blank_image = PhotoImage()
colors = ['white', 'red', 'green', 'white']

#Defining the Button function(s)

def button_click(hr_index, min_index):
	button = button_list[hr_index][min_index]
	bg = button.cget('bg')
	index = colors.index(bg)
	button_list[hr_index][min_index].config(bg=colors[index+1])
 
#Defining the grid buttons:

h=10 #height
w=10 #width
button_list = [] #List of button objects
def loadgrid(date):
        h=10 #height
        w=10 #width
        L=[]
        for x in fh.getrows():
                if x[0]==str(date):
                        for l in range(1,len(x),4):
                                L.append(x[l:l+4])

        for hr in range(0, 23+1):  #iterating throught the 24hrs of the day
                button_list.append([])
                for mins in range(0, 3+1):#iterating thru 4 15min slots of 1 hr
                        button_list[hr].append(Button(grid_frame, image=blank_image, height=h, width=w, bg=L[hr][mins] if fh.csv_isExist(date.today()) else 'white' , borderwidth=4, command=lambda h=hr, m=mins: button_click(h, m)))
        
loadgrid(date.today())


#Inserting the grid buttons

no_of_hrs = len(button_list)

for hr in range(no_of_hrs):
	no_of_minslots = len(button_list[hr])
	for mins in range(no_of_minslots):
		button_list[hr][mins].grid(row=mins+1, column=hr+1)

#Defining and inserting Grid Labels

#HR-labels
for i in range(24):
	hour = f"0{i}:00" if i<10 else f"{i}:00"

	sub_frame = LabelFrame(grid_frame)
	sub_frame.grid(row = 0, column = i+1)

	canvas_1_manage = Canvas(sub_frame, width = 10, height = 35)
	canvas_1_manage.pack()
	canvas_1_manage.create_text(6, 35, text = hour, angle = 90, anchor = "w")
#MIN-labels
for i in range(4):
	label_frame = LabelFrame(grid_frame, height=20, width=40)
	label_frame.grid(row=i+1, column=0)
	label_frame.pack_propagate(0) # Stops child widgets of label_frame from resizing it
	label = Label(label_frame, text ="{}-{}".format(i*15, (i+1)*15))
	label.pack()

#Clear all button

#func
def clear_all():
	for hrlist in button_list:
		for button in hrlist:
			button.config(bg='white') 
#code
clear_all = Button(grid_frame, text='Clear all', width=7, command=clear_all)
clear_all.grid(row=5, column=19, columnspan=3)

#Save button

#func
def _save_(): #Saves all the color values in the list activity_data
        activity_data = [] 
        no_of_hrs = len(button_list)
        for hr in range(no_of_hrs):
                activity_data.append([])
                no_of_minslots = len(button_list[hr])
                for mins in range(no_of_minslots):
                        button = button_list[hr][mins]
                        bg = button.cget('bg')
                        activity_data[hr].append(bg)
        #print(activity_data)
        flatlist=[date.today()]
        hp.reemovNestings(activity_data, flatlist)
        if len(fh.getrows())==1 or fh.csv_isExist(date.today()):
                print(fh.getrows())
                fh.csv_append(flatlist)
        else:
                fh.replace_row(date.today(), flatlist)	
			
#code
save = Button(grid_frame, text='Save', width=7, command=_save_)
save.grid(row=5, column=22, columnspan=3)


root.mainloop()
