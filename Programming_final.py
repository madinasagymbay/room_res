from tkinter import *
from tkinter import ttk
import sqlite3, csv
from datetime import datetime, timedelta

####################################################################################################################################
#1 PART 1 Extraction of data from a CSV
#Create a database
conn = sqlite3.connect("room_reservation.db")
cur = conn.cursor()

#Import csv data to database ONLY ONCE
'''
with open("room_reservation_headings.csv", "r") as file:
    for row in file:
        cur.execute("INSERT INTO BookingTable VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row.split(";"))
        conn.commit()
print("completed")
conn.close()
'''

####################################################################################################################################
#2 PART 2 Developing a search engine 
#Tkinter GUI      
root = Tk()

# PUT HERE COMMENT AND AT THE END WHERE SHOWN (TO EXPORTING CSV FILE TO SQLITE DATABASE )

#Creating a widget
label1 = Label(root, text = "ROOM RESERVATION\n  \nRoom search", font = ("Helvetica", 18, "bold"), justify = "left", foreground="darkblue").grid(row=5, column=0, sticky=NW)


#Quering the column name drom the db
query_column = cur.execute("SELECT * FROM BookingTable").fetchone()


#As the quered column name type is tuple, next step will be conversion to one-dimensional list
delimiter = ','
joined_query = delimiter.join(query_column)
column_list = list(joined_query.split(delimiter))


#Checking function that returns the final list that considers location, room name, type, capacity, equipment and available hours options and further proceed to show_info function
def check_info(location, room_name, room_type, list_room_name, capacity, equipment, at_least_one, time_slots):
    ###Creating list for all matched rooms for selected LOCATION
    all_room_name = conn.execute("SELECT room_name FROM BookingTable")
    list_all_rn = [r for r, in all_room_name] 
    del list_all_rn[0] #deleting title row "Select room..."
    
    location_matched_all = list_all_rn
    
    if location == "﻿Select location…":
        location_matched = list_all_rn
        #print(location_matched)
        #print("matched location: sel room name {}".format(location_matched))
    else:
        location_matched = list_room_name 
        #print("matched location: all room name {}".format(location_matched))
    
    
    ###Creating list for all matched rooms for selected ROOM NAME
    room_matched = []
    if location != "﻿Select location…":
        if room_name == "  ":
            room_matched = list_room_name
            #print("location selected: list_room_name".format(room_matched))
        else:
            #print("location selected: room_name".format(room_name))
            room_matched.append(room_name)
    else:
        #print("location not selected: list_all_rn")
        room_matched = list_all_rn
        
    ###Creating list for all matched rooms for selected ROOM TYPE
    if room_type == "Room type…":
        list_rt_match = list_all_rn 
    else:
        room_type_match = conn.execute('SELECT room_name FROM BookingTable WHERE room_type == "{}"'.format(room_type))
        list_rt_match = [r for r, in room_type_match] 
    #print("matched room type {}".format(list_rt_match))
    
        
    ###Creating list for all matched rooms for selected CAPACITY
    if capacity == "1-20":
        cap_matched = conn.execute("SELECT room_name FROM BookingTable WHERE cap_range == '0-20'")
        list_cap_match = [r for r, in cap_matched]
    elif capacity == "21-40":
        cap_matched = conn.execute("SELECT room_name FROM BookingTable WHERE cap_range == '21-40'")
        list_cap_match = [r for r, in cap_matched]
    elif capacity == "41-60":
        cap_matched = conn.execute("SELECT room_name FROM BookingTable WHERE cap_range == '41-60'")
        list_cap_match = [r for r, in cap_matched]
    elif capacity == "61-80":
        cap_matched = conn.execute("SELECT room_name FROM BookingTable WHERE cap_range == '61-80'")
        list_cap_match = [r for r, in cap_matched]
    elif capacity == "81-100":
        cap_matched = conn.execute("SELECT room_name FROM BookingTable WHERE cap_range == '81-100'")
        list_cap_match = [r for r, in cap_matched]
    elif capacity == "101-150":
        cap_matched = conn.execute("SELECT room_name FROM BookingTable WHERE cap_range == '101-150'")
        list_cap_match = [r for r, in cap_matched]
    elif capacity == ">150":
        cap_matched = conn.execute("SELECT room_name FROM BookingTable WHERE cap_range == '>150'")
        list_cap_match = [r for r, in cap_matched]
    else:
        list_cap_match = list_all_rn

    #print("matched capacity {}".format(list_cap_match))
    
    
    ###Creating list for all matched rooms for selected TIME SLOTS
    #Query to get and create a list from db
    query_started_date = "SELECT book_started_date FROM BookingTable"
    set_started_date = conn.execute(query_started_date)
    list_started_date = [r for r, in set_started_date] 
    #print(list_started_date)
    
    #Query to get and create a list from db
    query_ended_date = "SELECT book_ended_date FROM BookingTable"
    set_ended_date = conn.execute(query_ended_date)
    list_ended_date = [r for r, in set_ended_date] 
    #print(list_ended_date)
    
    matched_time = []
    
    if time_slots == "Time...":
        matched_time = list_all_rn
    else:
        ##
        start_date_list = []
        for i in range(1, len(list_started_date)):
            start_date_list.append(datetime.strptime(list_started_date[i], "%Y-%m-%d %H:%M"))
        #print(start_date_list)
        
        end_date_list = []
        for i in range(1, len(list_ended_date)):
            end_date_list.append(datetime.strptime(list_ended_date[i], "%Y-%m-%d %H:%M"))
        #print(end_date_list)
        hours = (datetime(2021, 1, 4, 9, 0), datetime(2021, 1, 4, 18, 0))
        
        indice = 0
        list_avail_hrs = []
        for i in range (0, len(start_date_list)):
            booked = [(start_date_list[i], end_date_list[i])]
            avail_hrs = get_slots(hours, booked, duration=timedelta(hours=1))
            list_avail_hrs.append(avail_hrs)
        #print(list_avail_hrs)
        ##
        
        #print(time_slots)
        index_rn = []
        for i,lst in enumerate(list_avail_hrs):
            for j, hrs in enumerate(lst):
                if hrs == time_slots:
                    index_rn.append(i)
        #print(index_rn)
        
        for i in index_rn:
            matched_time.append(list_all_rn[i])
        #print(matched_time)
        
        if __name__ == "__main__":
            get_slots(hours, booked)
        
        
    ###Creating list for all matched rooms for selected EQUIPMENT
    matched_equip = []
    if not equipment:
        matched_equip = list_all_rn
    else:
        ##
        delimiter = ','
        all_eq_per_room = []
        query_eq = conn.execute("SELECT * FROM BookingTable")
        q_eq_title = query_eq.fetchone()
    
        for i in list_all_rn:
            q_equip = query_eq.fetchone()
            joined_query = delimiter.join(q_equip)
            row_list = list(joined_query.split(delimiter))
            del row_list[:5]
            eq_per_room = row_list[:-3] #equipment availability per room in the form of "yes" and "no"
            all_eq_per_room.append(eq_per_room)
        
        for index, eqps in enumerate(all_eq_per_room):
            for item, eq in enumerate(eqps):
                if eq == "yes":
                    all_eq_per_room[index][item] = eq.replace(eq, eq_list[item])
        #print(all_eq_per_room)
        
        all_eq_per_room = [[eq for eq in eqps if eq != "no"] for eqps in all_eq_per_room]
        #print(all_eq_per_room)
        ##
        
        matched_equip_ind = []
        list_equip_ind = []
        if at_least_one == "yes":
            for index, eqps in enumerate(all_eq_per_room):
                for item, eqp in enumerate(eqps):
                    if eqp in equipment:
                        matched_equip_ind.append(index)
            matched_equip_ind = list(dict.fromkeys(matched_equip_ind))
            #print(matched_equip_ind)
            
            for i in matched_equip_ind:
                matched_equip.append(list_all_rn[i])
            #print(matched_equip)
            
        else:
            for index, eqps in enumerate(all_eq_per_room):
                for item, eqp in enumerate(eqps):
                    for i in equipment:
                        if i == eqp:
                            all_eq_per_room[index][item] = eq.replace(eq, "yes")
            all_eq_per_room = [[eq for eq in eqps if eq == "yes"] for eqps in all_eq_per_room]
            
            for index, eqps in enumerate(all_eq_per_room):
                if len(eqps) == len(equipment):
                    matched_equip_ind.append(index)
            for i in matched_equip_ind:
                matched_equip.append(list_all_rn[i])
            #print(matched_equip)  
    
    
    ###Creating list for all matched rooms for for ALL SELECTED CHOICES
    all_matched = []
    all_matched = set(location_matched_all).intersection(room_matched, list_cap_match, location_matched, list_rt_match, matched_time, matched_equip)
    print("Result: the suitable rooms are {}".format(all_matched))
    show_info(all_matched, list_all_rn)
    
#Function to identify available hours considering booked start and end dates              
def get_slots(hours, booked, duration=timedelta(hours=1)):
    slots = sorted([(hours[0], hours[0])] + booked + [(hours[1], hours[1])])
    avail_hrs = []
    for start, end in ((slots[i][1], slots[i+1][0]) for i in range(len(slots)-1)):
        assert start <= end, "Cannot attend all appointments"
        while start + duration <= end:
            avail_hrs.append("{:%H:%M}-{:%H:%M}".format(start, start + duration))
            #print ("{:%H:%M} - {:%H:%M}".format(start, start + duration))
            start += duration
    return(avail_hrs)
    

####################################################################################################################################
#3 PART 3 Adding a booking tool  
#Booking tool
#Function for booking the room and inserting data information to new db
def room_booking(room_num, hour_slot, curr_frame, row_num):

    conn_book = sqlite3.connect("room_booking.db")
    cur_book = conn_book.cursor()
    
    roomID = room_num
    date = datetime.today().strftime('%Y-%m-%d')
    hours = hour_slot
    frame_in_canvas = curr_frame
    indice = row_num
    
    print(roomID)
    print(date)
    print(hours)
    
    cur_book.execute("INSERT INTO BookingRecord (RoomID, date, hours) VALUES (?, ?, ?)", (roomID, date, hours))
    conn_book.commit()
    
    record_label = Label(frame_in_canvas, text = "Booking detail is recorded.", font = ("Helvetica", 13, "bold"), justify = "left", foreground="darkblue").grid(row=indice, column=9, sticky=NW)
    record_label2 = Label(frame_in_canvas, text = "To start new booking", font = ("Helvetica", 13, "bold"), justify = "left", foreground="darkblue").grid(row=indice+1, column=9, sticky=NW)
    record_label3 = Label(frame_in_canvas, text = "change the time slot", font = ("Helvetica", 13, "bold"), justify = "left", foreground="darkblue").grid(row=indice+2, column=9, sticky=NW)
    record_label4 = Label(frame_in_canvas, text = "and book", font = ("Helvetica", 13, "bold"), justify = "left", foreground="darkblue").grid(row=indice+3, column=9, sticky=NW)

def clicked_time(call, curr_frame, row_num, clicked_value):
    dic_clicked_per_room = {"Room index":"clicked value"}
    dic_clicked_per_room[clicked_value]=call
    
    label_warn = Label(curr_frame, text = "Please select the time", font = ("Helvetica", 13, "bold"), justify = "left", foreground="darkblue").grid(row=row_num, column=9, sticky=NW)
    
    #creating button for booking the room
    button_book = Button(curr_frame, text="BOOK NOW", command=lambda room_num=clicked_value, hour_slot=call, curr_frame=curr_frame, row_num=row_num: room_booking(room_num, hour_slot, curr_frame, row_num))
    button_book.grid(row=row_num, column=8, padx=30)
    
####################################################################################################################################
#4 PART 4 Displaying information about the selected room 
#Function that shows the result of searching tool in new window
def show_info(all_matched, list_all_rn):
    #Create main frame
    searchResult = Toplevel(root)
    searchResult.title("Result of search")
    searchResult.geometry("1300x500")
    
    #Create canvas
    canvas_results = Canvas(searchResult)
    canvas_results.pack(side=LEFT, fill=BOTH, expand=1)
    
    #Add a scrollbar to the canvas
    scrollbar = ttk.Scrollbar(searchResult, orient=VERTICAL, command=canvas_results.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    #Configure the canvas
    canvas_results.configure(yscrollcommand=scrollbar.set)
    canvas_results.bind("<Configure>", lambda e: canvas_results.configure(scrollregion=canvas_results.bbox("all")))
    
    #Create frame inside the canvas
    frame_in_canvas = Frame(canvas_results)
    
    #Add frame to a window in the canvas
    canvas_results.create_window((0,0), window=frame_in_canvas, anchor='nw')
    
    label2 = Label(frame_in_canvas, text = "SEARCH RESULT", font = ("Helvetica", 18, "bold"), justify = "left", foreground="darkblue").grid(row=1, column=0, sticky=NW)
    
    #Check whether the list from searching tool "all_matched" is empty or not
    if not all_matched:
        label3 = Label(frame_in_canvas, text = "No results found, please try again searching with other options", font = ("Helvetica", 16, "bold"), justify = "left", foreground="darkblue").grid(row=2, column=0, sticky=NW)
    else:
        #Create labels for main titles
        label3 = Label(frame_in_canvas, text = "Location", font = ("Helvetica", 15, "bold"), foreground="darkblue").grid(row=3, column=1)
        label4 = Label(frame_in_canvas, text = "Room type", font = ("Helvetica", 15, "bold"), foreground="darkblue").grid(row=3, column=2, padx=20)
        label5 = Label(frame_in_canvas, text = "Capacity", font = ("Helvetica", 15, "bold"), foreground="darkblue").grid(row=3, column=3, padx=20)
        label6 = Label(frame_in_canvas, text = "Room name", font = ("Helvetica", 15, "bold"), foreground="darkblue").grid(row=3, column=0, sticky=NW)
        label7 = Label(frame_in_canvas, text = "Equipment", font = ("Helvetica", 15, "bold"), foreground="darkblue").grid(row=3, column=4)
        label8 = Label(frame_in_canvas, text = "Available hours", font = ("Helvetica", 15, "bold"), foreground="darkblue").grid(row=3, column=5)
        label9 = Label(frame_in_canvas, text = "Found {} rooms".format(len(all_matched)), font = ("Helvetica", 15, "bold"), justify = "left", foreground="darkblue").grid(row=2, column=0, sticky=NW)
        indice = 4
        list_eq_click = []
        for i in all_matched:
            label3 = Label(frame_in_canvas, text = i, font = ("Helvetica", 13, "bold"), justify = "left", foreground="darkblue").grid(row=indice, column=0, sticky=NW)
            
            #identifying room location info and creating label
            location_info_q = conn.execute('SELECT location FROM BookingTable WHERE room_name == "{}"'.format(i))
            location_info = location_info_q.fetchone()
            location_info = location_info[0]
            
            label_loc = Label(frame_in_canvas, text = "{}".format(location_info), font = ("Helvetica", 13), foreground="darkblue").grid(row=indice, column=1)
            
            #identifying room type info and creating label
            room_type_info_q = conn.execute('SELECT room_type FROM BookingTable WHERE room_name == "{}"'.format(i))
            room_type_info = room_type_info_q.fetchone()
            room_type_info = room_type_info[0]
            
            label_rt = Label(frame_in_canvas, text = "{}".format(room_type_info), font = ("Helvetica", 13), foreground="darkblue").grid(row=indice, column=2)
            
            #identifying room capacity info and creating label
            cap_info_q = conn.execute('SELECT capacity FROM BookingTable WHERE room_name == "{}"'.format(i))
            cap_info = cap_info_q.fetchone()
            cap_info = cap_info[0]
            
            label_cap = Label(frame_in_canvas, text = "{}".format(cap_info), font = ("Helvetica", 13), foreground="darkblue").grid(row=indice, column=3)
            
            #identifying room index
            for index, room in enumerate(list_all_rn):
                if i == room:
                    index_room = index
                    
            #list_eq_click.append(index_room) #list of all suitable rooms' indexes


            #identifying list of equipment per room
            delimiter = ','
            all_eq_per_room = []
            query_eq = conn.execute("SELECT * FROM BookingTable")
            q_eq_title = query_eq.fetchone()
        
            for i in list_all_rn:
                q_equip = query_eq.fetchone()
                joined_query = delimiter.join(q_equip)
                row_list = list(joined_query.split(delimiter))
                del row_list[:5]
                eq_per_room = row_list[:-3] #equipment availability per room in the form of "yes" and "no"
                all_eq_per_room.append(eq_per_room)
            
            for index, eqps in enumerate(all_eq_per_room):
                for item, eq in enumerate(eqps):
                    if eq == "yes":
                        all_eq_per_room[index][item] = eq.replace(eq, eq_list[item])
            all_eq_per_room = [[eq for eq in eqps if eq != "no"] for eqps in all_eq_per_room]

            #finding equipment list for room using index
            eq_info = all_eq_per_room[index_room]
            
            #creating label for each equipment 
            for i in range(len(eq_info)):
                label_eq = Label(frame_in_canvas, text = "{}".format(eq_info[i]), font = ("Helvetica", 13), foreground="darkblue").grid(row=i+indice, column=4)
            
            
            #identifying list of available hours per room
            start_date_list = []
            for i in range(1, len(list_started_date)):
                start_date_list.append(datetime.strptime(list_started_date[i], "%Y-%m-%d %H:%M"))
            
            end_date_list = []
            for i in range(1, len(list_ended_date)):
                end_date_list.append(datetime.strptime(list_ended_date[i], "%Y-%m-%d %H:%M"))

            hours = (datetime(2021, 1, 4, 9, 0), datetime(2021, 1, 4, 18, 0))

            list_avail_hrs = []
            for i in range (0, len(start_date_list)):
                booked = [(start_date_list[i], end_date_list[i])]
                avail_hrs = get_slots(hours, booked, duration=timedelta(hours=1))
                list_avail_hrs.append(avail_hrs)
            
            #finding available hours list for room using index
            avail_hrs_info = list_avail_hrs[index_room]
            
            clicked4 = StringVar()
            clicked4.set(avail_hrs_info[0])
            
            #creating button for booking the room
            button_book = Button(frame_in_canvas, text="BOOK NOW", command=lambda call=clicked4.get(), curr_frame=frame_in_canvas, row_num=indice, clicked_value=index_room: clicked_time(call, curr_frame, row_num, clicked_value))
            button_book.grid(row=indice, column=8, padx=40)
            
            #Creating dropdown menu widget for each available hours
            
            avail_hrs_menu = OptionMenu(frame_in_canvas, clicked4, *avail_hrs_info, command=lambda call=index_room, curr_frame=frame_in_canvas, row_num=indice, clicked_value=index_room: clicked_time(call, curr_frame, row_num, clicked_value))
            avail_hrs_menu.grid(row=indice, column=5)
            

            
            
            #creating space between rooms
            label_space = Label(frame_in_canvas, text = "\n", font = ("Helvetica", 13), foreground="darkblue").grid(row=indice+10, column=0)
            
            indice += 11
    
#Function that sets conditions for check_info function
def search_func():
    #getting selected options from dropdown menu and buttons
    location = combo_location.get()
    #print(location)
    room_name = combo_room_name.get()
    #print(room_name)
    equipment = list_selected
    #print(equipment)
    room_type = clicked1.get()
    #print(room_type)
    capacity = clicked2.get()
    #print(capacity)
    time_slots = clicked3.get()
    #print(time_slots)
    at_least_one = var_one.get()
    #print(at_least_one)
    
    #Create a list for room names for selected location
    query_room_name = 'SELECT room_name FROM BookingTable WHERE location == "{}"'.format(combo_location.get())
    set_room_name = conn.execute(query_room_name)
    list_room_name = [r for r, in set_room_name]
    
    #Checking whether the location was selected or not to further proceed to check_info function
    if location != "﻿Select location…":
        if room_name == "  ":
            check_info(location, room_name, room_type, list_room_name, capacity, equipment, at_least_one, time_slots)
            print("location selected, room not: check info")
        elif room_name not in list_room_name:
            room_name = "  "
            check_info(location, room_name, room_type, list_room_name, capacity, equipment, at_least_one, time_slots)
            print("location selected, room not: check info")
        else:
            print("location selected, room too:show info")
            check_info(location, room_name, room_type, list_room_name, capacity, equipment, at_least_one, time_slots)
            #show_info(room_type, capacity, equipment, at_least_one, time_slots)
    else:
        check_info(location, room_name, room_type, list_room_name, capacity, equipment, at_least_one, time_slots)
        print("location not selected: check info")


#Creating searching button
button_search = Button(root, text="SEARCH", command=search_func)
button_search.grid(row=17, column=2)


####################################################################################################################################
#5 PART 5 Developing widgets for search engine  
#Creating LOCATION dropdown menu
#Query to get and create a list from db
query_location = "SELECT distinct(location) as location FROM BookingTable"
set_location = conn.execute(query_location)
list_location = [r for r, in set_location] 


#Creating dropdown menu widget
label_location = Label(root, text = "Location", font = ("Helvetica", 13), justify = "left").grid(row=7, column=0)
combo_location = ttk.Combobox(root, value = list_location, state = "readonly")
combo_location.bind("<<ComboboxSelected>>", search_func)
combo_location.grid(row=8, column=0)
combo_location.current(0)



#################################
#Creating ROOM NAME dropdown menu

#Function to pick ROOM NAME
def pick_room_name(e):
    query_room_name = 'SELECT room_name FROM BookingTable WHERE location == "{}"'.format(combo_location.get())
    set_room_name = conn.execute(query_room_name)
    list_room_name = [r for r, in set_room_name]
    combo_room_name.config(value = list_room_name)

#Binding LOCATION with ROOM NAME
combo_location.bind("<<ComboboxSelected>>", pick_room_name)

#Creating dropdown menu widget
label_room_name = Label(root, text = "Room name", font = ("Helvetica", 13), justify = "left").grid(row=7, column=1)
combo_room_name = ttk.Combobox(root, value = ["  "], state = "readonly")
combo_room_name.grid(row=8, column=1)
combo_room_name.current(0)


#################################
#Creating ROOM TYPE dropdown menu
#Query to get and create a list from db
query_room_type = "SELECT distinct(room_type) as room_type FROM BookingTable"
set_room_type = conn.execute(query_room_type)
list_room_type = [r for r, in set_room_type] 

#Creating dropdown menu widget
clicked1 = StringVar()
clicked1.set(list_room_type[0])
label_room_type = Label(root, text = "Room type", font = ("Helvetica", 13), justify = "left").grid(row=7, column=2)
room_type_menu = OptionMenu(root, clicked1, *list_room_type).grid(row=8, column=2)

#################################
#Creating CAPACITY dropdown menu
#List of capacity ranges
list_capacity = [
"Capacity...",
"1-20",
"21-40",
"41-60",
"61-80",
"81-100",
"101-150",
">150"   
]

#Creating dropdown menu widget
clicked2 = StringVar()
clicked2.set(list_capacity[0])
label_capacity = Label(root, text = "Capacity", font = ("Helvetica", 13), justify = "left").grid(row=7, column=3)
capacity_menu = OptionMenu(root, clicked2, *list_capacity).grid(row=8, column=3)

#################################
#Creating TIME-SLOTS dropdown menu
#List of time slots ranges
list_time = [
"Time...",
"09:00-10:00",
"10:00-11:00",
"11:00-12:00",
"12:00-13:00",
"13:00-14:00",
"14:00-15:00",
"15:00-16:00",
"16:00-17:00",
"17:00-18:00"
]

#Creating dropdown menu widget
clicked3 = StringVar()
clicked3.set(list_time[0])
label_time = Label(root, text = "Time slots", font = ("Helvetica", 13), justify = "left").grid(row=7, column=4)
time_menu = OptionMenu(root, clicked3, *list_time).grid(row=8, column=4)

#Query to get and create a list from db
query_started_date = "SELECT book_started_date FROM BookingTable"
set_started_date = conn.execute(query_started_date)
list_started_date = [r for r, in set_started_date] 
#print(list_started_date)

query_ended_date = "SELECT book_ended_date FROM BookingTable"
set_ended_date = conn.execute(query_ended_date)
list_ended_date = [r for r, in set_ended_date] 
#print(list_ended_date)

    

#################################
#Creating equipment selection label
label_space = Label(root, text = "  ", ).grid(row=10, column=0)
label_equipment = Label(root, text = "Equipment type", font = ("Helvetica", 13), justify = "left").grid(row=12, column=0, sticky=NW)
      
#Creating equipment checklist with for loop
eq_list = column_list.copy()
del eq_list[:5] #Deleting first 4 columns
eq_list = eq_list[:-3]
#print(eq_list)

#Function to react on click and add selected boxes to the list_selected
def on_clicked(column, indice):
    if check_state[indice].instate(['selected']) == True:
        list_selected.append(column)
    else:
        list_selected.remove(column)
    #print(list_selected)

#Function to create checkbutton for each row
def create_button(indice, eq, row_num):
    checkbox = ttk.Checkbutton(root, text = eq, command=lambda i=indice, call=eq: on_clicked(call, i))
    check_state.append(checkbox)
    check_state[indice].grid(row = row_num, column = col_num, sticky=NW)
    check_state[indice].state(['!alternate'])

#Creation of checkbutton
list_selected = []
check_state = []
indice = 0
col_num = 0
row_num = 13

for eq in eq_list[0: 4]:
    create_button(indice, eq, row_num)
    indice += 1
    col_num += 1
    
col_num = 0
row_num += 1
for eq in eq_list[4: 8]:
    create_button(indice, eq, row_num)
    indice += 1
    col_num += 1
    
col_num = 0
row_num += 1
for eq in eq_list[8: 12]:
    create_button(indice, eq, row_num)
    indice += 1
    col_num += 1     

#Creating choice for finding room with at least one of the selected equipment or all selected items must present in the room
var_one = StringVar()
check_one = Checkbutton(root, text = "At least one equipment should present", variable = var_one, onvalue = "yes", offvalue = "no")
check_one.grid(row=15, column=3, sticky=NW)



# PUT HERE COMMENT

root.mainloop()

