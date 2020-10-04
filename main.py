from tkinter import *
from datetime import date
import file_handling as fh
import help_functions as hp
import os

fill_mode = False
fill_color = 'red'

#activity_data = [] #stores the color values of all timeslots/Button UPON SAVING

#print(date.fromisoformat(str(date.today())).weekday())
if os.path.exists('data.csv') == False:
	fh.initialize()

root = Tk()
root.title("Time Matrix")

grid_frame = LabelFrame(root, padx=10, pady=10)
grid_frame.pack()

blank_image = PhotoImage()
colors = ['white', 'red', 'blue', 'green', 'white']

#Defining the Button function(s)

def button_click(hr_index, min_index):
    button = button_list[hr_index][min_index]
    if fill_mode:
        button_list[hr_index][min_index].config(bg=fill_color)
    else:        
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
        p=False
        for x in fh.getrows():
                if x[0]==str(date):
                        p=True
                        for l in range(1,len(x),4):
                                L.append(x[l:l+4])

        for hr in range(0, 23+1):  #iterating throught the 24hrs of the day
                button_list.append([])
                for mins in range(0, 3+1):#iterating thru 4 15min slots of 1 hr
                        button_list[hr].append(Button(grid_frame, image=blank_image, height=h, width=w, bg=L[hr][mins] if p else 'white', borderwidth=4, command=lambda h=hr, m=mins: button_click(h, m)))
        
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

#File-Mode:

#label
filemode_frame = LabelFrame(grid_frame, width=60, height=27)
filemode_frame.grid(row=5, column=1, columnspan=3)
filemode_frame.pack_propagate(0)
_filemode = Label(filemode_frame, text='Fill Mode:')
_filemode.pack()

#toggle-button
def fmt(): #Fill mode toggle button function
    b = FM_toggle_button
    text = b.cget('text')
    if text=='Off':
        b.configure(bg=fill_color)
        b.configure(text="On")
    elif text=="On":
        b.configure(bg='grey')
        b.configure(text="Off")    

FM_toggle_button = Button(grid_frame, text='Off', bg='grey', command=fmt)
FM_toggle_button.grid(row=5, column=4, columnspan=2, sticky=N+S+E+W)

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
        #print(fh.csv_isExist(str(date.today())))
        if fh.csv_isExist(str(date.today())):
                fh.replace_row(date.today(), flatlist)	
        else:
                fh.csv_append(flatlist)
			
#code
save = Button(grid_frame, text='Save', width=7, command=_save_)
save.grid(row=5, column=22, columnspan=3)


root.mainloop()
