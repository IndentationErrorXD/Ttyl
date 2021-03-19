from tkinter import *
from tkinter import messagebox
import tkinter.font as tkfont
from tkcalendar import DateEntry
from datetime import date, datetime, timedelta
import file_handling as fh
import help_functions as hp
import os

fill_mode = False
fill_color = 'red'
colors = ['white', 'red', 'orange', 'blue', 'green', 'yellow','white']
date = date.today()
unsaved_changes=False

#activity_data = [] #stores the color values of all timeslots/Button UPON SAVING

#print(date.fromisoformat(str(date.today())).weekday())
if os.path.exists('data.csv') == False:
	fh.initialize()

root = Tk()
root.title("Time Matrix")

blank_image = PhotoImage()

grid_frame = LabelFrame(root, padx=10, pady=10)
grid_frame.grid(row=0, column=0, columnspan=25, rowspan=6)

#Defining the Button function(s)

def button_click_default(hr_index, min_index):
    global unsaved_changes
    button = button_list[hr_index][min_index]
    bg = button.cget('bg')
    index = colors.index(bg)
    button_list[hr_index][min_index].config(bg=colors[index+1])
    unsaved_changes=True

def button_click_fill_mode(hr_index, min_index, fill_color):
    global unsaved_changes
    button = button_list[hr_index][min_index]      
    button.config(bg=fill_color)  
    unsaved_changes=True  

#Defining the grid buttons:

h=10 #height
w=10 #width
button_list = [] #List of button objects
def loadgrid(date, data=[]):
        #print(dat)
        global fill_mode
        global fill_color

        h=10 #height
        w=10 #width
        L=data
        p=False
        if L!=[]:
            p=True
        else:    
            for x in fh.getrows():
                    if x[0]==str(date):
                            p=True
                            for l in range(1,len(x),4):
                                    L.append(x[l:l+4])                            
                          
        for hr in range(0, 23+1):  #iterating throught the 24hrs of the day
                button_list.append([])
                for mins in range(0, 3+1):#iterating thru 4 15min slots of 1 hr
                    if fill_mode:
                        #print('fill mode called')
                        button_list[hr].append(Button(grid_frame, image=blank_image, height=h, width=w, bg=L[hr][mins] if p else 'white', borderwidth=4, command=lambda h=hr, m=mins, color=fill_color: button_click_fill_mode(h, m, color)))
                    else:
                        #print('def mode called')    
                        button_list[hr].append(Button(grid_frame, image=blank_image, height=h, width=w, bg=L[hr][mins] if p else 'white', borderwidth=4, command=lambda h=hr, m=mins: button_click_default(h, m)))
        
loadgrid(date)

#Inserting the grid buttons
def insertgrid(button_list):
    no_of_hrs = len(button_list)

    for hr in range(no_of_hrs):
    	no_of_minslots = len(button_list[hr])
    	for mins in range(no_of_minslots):
    		button_list[hr][mins].grid(row=mins+1, column=hr+1)

insertgrid(button_list)

#Deleting the grid buttons
def deletegrid():
    no_of_hrs = len(button_list)

    for hr in range(no_of_hrs):
        no_of_minslots = len(button_list[hr])
        for mins in range(no_of_minslots):
            button_list[hr][mins].destroy()

#Refreshing the grid 
def refresh_grid():
    global button_list

    #caching grid in activity data
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
                     
    deletegrid()
    button_list=[]
    loadgrid(date, activity_data)
    insertgrid(button_list)

#Defining and inserting Grid Labels

#HR-labels

for i in range(12):
	l = [12]+list(range(1,12))
	e=l[i]
	hour = f"0{e}:00  AM" if e<10 else f"{e}:00  AM"

	sub_frame = LabelFrame(grid_frame)
	sub_frame.grid(row = 0, column = i+1)

	canvas_1_manage = Canvas(sub_frame, width = 10, height = 60)
	canvas_1_manage.pack()
	canvas_1_manage.create_text(6, 60, text = hour, angle = 90, anchor = "w")

for i in range(12):
	l = [12]+list(range(1,12))
	e=l[i]
	hour = f"0{e}:00  PM" if e<10 else f"{e}:00  PM"

	sub_frame = LabelFrame(grid_frame)
	sub_frame.grid(row = 0, column = 12+i+1)

	canvas_1_manage = Canvas(sub_frame, width = 10, height = 60)
	canvas_1_manage.pack()
	canvas_1_manage.create_text(6, 60, text = hour, angle = 90, anchor = "w")

#MIN-labels
for i in range(4):
	mins_frame = LabelFrame(grid_frame, height=20, width=40)
	mins_frame.grid(row=i+1, column=0)
	mins_frame.pack_propagate(0) # Stops child widgets of label_frame from resizing it
	min_label = Label(mins_frame, text ="{}-{}".format(i*15, (i+1)*15))
	min_label.pack()

#Fill-Mode:

#label
fillmode_frame = LabelFrame(grid_frame, width=60, height=27)
fillmode_frame.grid(row=5, column=1, columnspan=3)
fillmode_frame.pack_propagate(0)
_fillmode = Label(fillmode_frame, text='Fill Mode:')
_fillmode.pack()

#toggle-button
def fmt(): #Fill mode toggle button function
    global button_list
    global fill_mode
    b = FM_toggle_button
    bc = FC_toggle_button
    text = b.cget('text')
    #print(f'Text="{text}"')
    if text=='Off':
        fill_mode=True
        FC_toggle_button.configure(state='normal')
        bc.config(bg='red')
        bc.config(text='red')
        b.config(text="On")

        refresh_grid()

    elif text=="On":
        fill_mode=False
        bc.config(bg='light grey')
        bc.config(state='disabled')
        b.config(text="Off")

        refresh_grid()
    else:
        print('DEVELOPER ERROR')       

FM_toggle_button = Button(grid_frame, text='Off', bg='light grey', command=fmt)
FM_toggle_button.grid(row=5, column=4, columnspan=3, sticky=N+S+E+W)

#Fill-Color

#label
fillcolor_frame = LabelFrame(grid_frame, width=60, height=27)
fillcolor_frame.grid(row=6, column=1, columnspan=3)
fillcolor_frame.pack_propagate(0)
_fillcolor = Label(fillcolor_frame, text='Fill Color:')
_fillcolor.pack()

#button
def fcf(): #Fill color function
    global button_list
    global fill_color
    b=FC_toggle_button
    bg = b.cget('bg')
    index = colors.index(bg)
    next_color=colors[index+1]
    capitalized_next_color = next_color[0].upper() + next_color[1::]
    fill_color=next_color
    b.config(bg=next_color)
    b.config(text=next_color) 

    refresh_grid()   

FC_toggle_button = Button(grid_frame, text=fill_color, bg='light grey', command=fcf, state=DISABLED)
FC_toggle_button.grid(row=6, column=4, columnspan=3, sticky=N+S+E+W)


#Clear all button

#func
def clear_all():
    global unsaved_changes
    for hrlist in button_list:
        for button in hrlist:
            button.config(bg='white')
    unsaved_changes=True         

#code
clear_all = Button(grid_frame, text='Clear all', width=7, command=clear_all)
clear_all.grid(row=5, column=19, columnspan=3)

#Save button

#func
def _save_(): #Saves all the color values in the list activity_data	
    global unsaved_changes
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
    flatlist=[date]
    hp.reemovNestings(activity_data, flatlist)
    #print(fh.csv_isExist(str(date.today())))
    if fh.csv_isExist(str(date)):
            fh.replace_row(date, flatlist)  
    else:
            fh.csv_append(flatlist)		
    unsaved_changes=False   

#code
save = Button(grid_frame, text='Save', width=7, command=_save_)
save.grid(row=5, column=22, columnspan=3)

color_info = Label(grid_frame, font=tkfont.Font(size=7),text="🛈 Green: Studied, Red: Wasted, Blue: Class, Yellow: Daily Activities, Orange: Sleep")
color_info.grid(row=6, column=7, columnspan=18, sticky='ES')





'''
Date-Picker
'''
def when_date_changed(e):
    global button_list
    global unsaved_changes
    global date

    _date=cal.get_date()

    if _date>date.today():
    	cal.set_date(date)
    	messagebox.showwarning('Time travel Not possible', "Cannot select future date")
    else:
        
        if unsaved_changes==True:
            save_qn = messagebox.askyesno('Confirm Save', "Save changes?")
            if save_qn==True:
                _save_()
            elif save_qn==False:
                unsaved_changes=False
             
        date = _date
        print(date)

        deletegrid()
        button_list=[]
        loadgrid(date, data=[])
        insertgrid(button_list)

picker_frame = LabelFrame(root)
picker_frame.grid(row=7, column=0, columnspan=25)

cal = DateEntry(picker_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
cal.grid(row=0, column=1, padx=10)
cal.bind('<<DateEntrySelected>>', when_date_changed)
cal.set_date(date)

def r_arrow():
    global date
    _date = date+timedelta(1)
    cal.set_date(_date)
    when_date_changed(0)

r_arrow = Button(picker_frame, text='🢂', command=r_arrow)
r_arrow.grid(row=0, column=2)

def l_arrow():
    global date
    _date = date - timedelta(1)
    cal.set_date(_date)
    when_date_changed(0)

l_arrow = Button(picker_frame, text='🢀', command=l_arrow)
l_arrow.grid(row=0, column=0)

'''
Analytics
'''

analytics_frame = LabelFrame(root, text='Analytics', padx=10, pady=10)
analytics_frame.grid(row=1, column=26, columnspan=2, rowspan=10)

from_lbl = Label(analytics_frame, text='From:')
to_lbl = Label(analytics_frame, text='To:')
days_f = Label(analytics_frame, text="Days filled:")
study = Label(analytics_frame, text="Studied:")
waste = Label(analytics_frame, text="Relaxing:")
_class= Label(analytics_frame, text="Class Hours:")
d_activities= Label(analytics_frame, text="Daily activities:")
sleep = Label(analytics_frame, text='Sleep:')
unfill = Label(analytics_frame, text="Unfilled:")

n=3
align = 'W'
from_lbl.grid(row=1, column=0,sticky=W)
to_lbl.grid(row=1, column=1, sticky=W)
days_f.grid(row=n,column=0, sticky=align)
study.grid(row=n+1,column=0, sticky=align)
waste.grid(row=n+2,column=0, sticky=align)
_class.grid(row=n+3,column=0, sticky=align)
d_activities.grid(row=n+4,column=0, sticky=align)
sleep.grid(row=n+5, column=0, sticky=align)
unfill.grid(row=n+6, column=0, sticky=align)
#--------------------------------------------------------------

start_date = date-timedelta(7)
end_date = date

_days_count = Label(analytics_frame, text='0')
_study_count = Label(analytics_frame, text='00hrs 00mins')
_waste_count = Label(analytics_frame, text='00hrs 00mins')
_class_count= Label(analytics_frame, text='00hrs 00mins')
_da_count= Label(analytics_frame, text='00hrs 00mins')
_sleep_count = Label(analytics_frame, text='00hrs 00mins')
_unfill_count = Label(analytics_frame, text='00hrs 00mins')

n=3
_days_count.grid(row=n, column=1)
_study_count.grid(row=n+1, column=1)
_waste_count.grid(row=n+2, column=1)
_class_count.grid(row=n+3, column=1)
_da_count.grid(row=n+4, column=1)
_sleep_count.grid(row=n+5, column=1)
_unfill_count.grid(row=n+6, column=1)

def refresh_analytics():
    global start_date
    global end_date
    range_in_focus = []

    study_count, waste_count, class_count, da_count, unfill_count, sleep_count, total = 0,0,0,0,0,0,0

    rows = fh.getrows()
    for row in rows:
        date = datetime.strptime(row[0], '%Y-%m-%d').date()
        if start_date<=date<=end_date:
            range_in_focus.append(row)

    days_filled=len(range_in_focus)
    
    for rows in range_in_focus:
        for x in rows:
            total+=1
            if x=='green':
                study_count+=1
            elif x=='red':
                waste_count+=1
            elif x=='blue':
                class_count+=1
            elif x=='yellow':
                da_count+=1
            elif x=='orange':
                sleep_count+=1    
            elif x=='white':
                unfill_count+=1

    def slots_to_time(num):
        hrs = num*15//60
        mins = (num*15)%60
        return f"{hrs}hrs {mins}mins"
    
    _days_count.config(text=days_filled)
    _study_count.config(text=slots_to_time(study_count)+f"  ({round((study_count*100/total),2) if total!=0 else 0}%)")
    _waste_count.config(text=slots_to_time(waste_count)+f"  ({round((waste_count*100/total),2) if total!=0 else 0}%)")
    _class_count.config(text=slots_to_time(class_count)+f"  ({round((class_count*100/total),2) if total!=0 else 0}%)")
    _da_count.config(text=slots_to_time(da_count)+f"  ({round((da_count*100/total),2) if total!=0 else 0}%)")
    _sleep_count.config(text=slots_to_time(sleep_count)+f"  ({round((sleep_count*100/total),2) if total!=0 else 0}%)")
    _unfill_count.config(text=slots_to_time(unfill_count)+f"  ({round((unfill_count*100/total),2) if total!=0 else 0}%)")

    return [study_count, waste_count, class_count, da_count, unfill_count, sleep_count, total]

refresh_analytics()

refresh = Button(analytics_frame, text="Refresh", command=refresh_analytics)
refresh.grid(row=10, column=1, sticky='ES', columnspan=2)

#Calendars

def from_cal_changed(e):
    print("From cal changed")
    global start_date
    _date=from_cal.get_date()

    if _date>date.today():
    	from_cal.set_date(start_date)
    	messagebox.showwarning('Time travel Not possible', "Cannot select future date")
    elif _date>end_date:
        from_cal.set_date(start_date)
        messagebox.showwarning("User Error", "From date cannot exceed To-date.\nPlease set to-date first")
    else:
        start_date=_date
        refresh_analytics()

def to_cal_changed(e):
    print("To cal changed")
    global end_date
    _date=to_cal.get_date()

    if _date>date.today():
    	to_cal.set_date(end_date)
    	messagebox.showwarning('Time travel Not possible', "Cannot select future date")
    elif _date<start_date:
        to_cal.set_date(end_date)
        messagebox.showwarning("User Error", "From date cannot preceed from-date.\nPlease set from-date first")
    else:
        end_date=_date
        refresh_analytics()

#from:
from_cal = DateEntry(analytics_frame, width=10, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
from_cal.grid(row=2, column=0)
from_cal.set_date(start_date)
from_cal.bind('<<DateEntrySelected>>', from_cal_changed)

#to:
to_cal = DateEntry(analytics_frame, width=10, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
to_cal.grid(row=2, column=1)
to_cal.set_date(end_date)
to_cal.bind('<<DateEntrySelected>>', to_cal_changed)

root.mainloop()
