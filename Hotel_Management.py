# First of all we import the necesaary modules
# Then we connet to MYSQL
# After that we create a function which calls the data from mysql to python and call it
# After it we create the sub-functions of main-function which will be called by the main function 
# After it we create the main function thorugh which our program runs
# In last after the welcome line we calls our main function
# Here user is the person whois operating this program and customer is the person who wants facilities in hotel

#importing statements
import mysql.connector as msc
import pandas as pd
from datetime import datetime
import time
import calendar
from fpdf import FPDF
import os
import matplotlib.pyplot as plt

# Here we used try-except conditional statements
try:
    # We ask user his/her mysql password for making connection of program to mysql
    mysql_paswrd = input("Enter password of your MySQL: ")

    # Here we tried to connect in existing parking database in this try loop if it was created previously
    mysql_obj = msc.connect(host = "localhost",
                            user = "root",
                            passwd = mysql_paswrd,
                            database = "Hotel_Management",
                            charset = 'utf8')
    mysql_crsr = mysql_obj.cursor()
    mysql_crsr.execute("use Hotel_Management;")
except:
    # If database would not found then we create a new database in this except loop    
    mysql_obj = msc.connect(host = "localhost",
                            user = "root",
                            passwd = mysql_paswrd,
                            database = "mysql",
                            charset = 'utf8')
    mysql_crsr = mysql_obj.cursor()
    mysql_crsr.execute("create database Hotel_Management;")
    mysql_crsr.execute("use Hotel_Management;")

    # Here we create Room-Records table
    mysql_crsr.execute("create table Room_Records(Room_No int Primary Key, Capacity int,Room_Type varchar(32),Minimum_ChargeX24 int, Status varchar(6));")
    # We add some dumy data here
    mysql_crsr.execute("insert into Room_Records values(1, 2, 'Normal', 600, 'Free'),(2, 2, 'Normal', 600, 'Free'),(3, 4, 'Normal', 1200, 'Free'),(4, 4, 'Normal', 1200, 'Free'),(5, 2, 'Delux', 800, 'Booked'),(6, 2, 'Delux', 800, 'Free'),(7, 4, 'Delux', 1600, 'Free'),(8, 4, 'Delux', 1600, 'Free'),(9, 2, 'Super-Delux', 1000, 'Free'),(10, 2, 'Super-Delux', 1000, 'Free'),(11, 4, 'Super-Delux', 1800, 'Booked'),(12, 4, 'Super-Delux', 1800, 'Free'),(13, 6, 'Normal', 1800, 'Free'),(14, 6, 'Delux', 2200, 'Free'),(15, 8, 'Normal', 2200, 'Free'),(16, 8, 'Delux', 2500, 'Free');")

    # Here we create Customer-Records table
    mysql_crsr.execute("create table Customer_Records(Customer_No int Primary Key, Name varchar(48),Contact_No varchar(16), Customer_ID varchar(24), ID_Number varchar(48), Checkin_Time datetime, Checkout_Time datetime, Persons int, Room_No int,Paid_Amount int, Left_Amount int, Status varchar(7));")
    # Inserting data in Customer-Records table
    mysql_crsr.execute("insert into Customer_Records values(1, 'Vikas', '9414777777', 'Aadhar Card', '895298984455', '2021-01-06 10:20:20', '2021-01-07 11:40:50', 1, 1,600,0,'Left'),(2, 'Aman', '8825500000', 'Pan Card', '12CCF23124HH','2021-01-07 16:15:44', '2021-01-08 10:46:10', 3, 8,1600,0,'Left'),(3, 'Rekha', '67545635353', 'Aadhar Card', '2342235643836','2021-01-08 16:17:12', '2021-01-09 05:46:10', 5, 13,1800,0,'Left'),(4, 'Pankaj', '8923232323', 'License', 'RJ13343GH435','2021-01-09 16:19:36', '2021-01-11 11:19:36', 1, 1,1200,0,'Left'),(5, 'Karishma', '3426472342', 'Aadhar Card', '456484884353','2021-01-22 16:21:33', '0000-00-00 00:00:00', 4, 11,1800,0,'Staying'),(6, 'Akshay', '342669234', 'Aadhar card', '343537892368','2021-01-22 16:23:09', '2021-01-23 12:21:33', 2, 6,800,0,'Left'),(7, 'Soniya', '7685683434', 'Passport', '346912790345','2021-01-23 16:24:08', '0000-00-00 00:00:00', 1, 5,800,0,'Staying');")  

    #For saving all the above creation/changes in MySQL permanently
    mysql_obj.commit()


# Here we define this function that calls data from mysql server
def fetch_mysql():
    mysql_crsr.execute("select * from Room_Records;")
    # As variables in def function are local so we have to make them gloabal for using them outside the def
    global room_records
    room_records = mysql_crsr.fetchall()
    mysql_crsr.execute("select * from Customer_Records;")
    global customer_records
    customer_records = mysql_crsr.fetchall()

# We call the above function, as the function defining below use the data from mysql that is introduced above
fetch_mysql()

# We define this sub-function of main function which runs on main function call, this function will do the functionality of main-function i.e. View  Room Records - 1st
def view_rooms():
    # Converting the fetched data from mysql into tabluar form to show
    rooms_table = pd.DataFrame(room_records, columns=['Room_No', 'Capacity', 'Room_Type', 'Minimum_ChargeX24', 'Status'])
    print("\nRoom Records....\n")
    print(rooms_table)
    print("\n")

    # After completion of this function we call the main function in it so that it will run unbreakably
    main_function()

# This is sub-function of main function which runs on main function call, this function will do the functionality of main-function i.e. View  Customer Records - 2nd
def customer_data():
    # Converting the fetched data from mysql into tabluar form to show
    customer_table = pd.DataFrame(customer_records, columns=['Customer_No', 'Name', 'Contact_No', 'Customer_ID', 'ID_Number', 'Checkin_Time', 'Checkout_Time', 'Persons', 'Room_No', 'Paid_Amount', 'Left_Amount', 'Status'])
    print("\nCustomer Records....\n")
    print(customer_table)
    print("\n")
    main_function()

# This is sub-function of main function which runs on main function call, here we define the functionality i.e. adding new entery in lending records - 3rd
def checkin_entery():
    print("\nHotel Check_In Entery....\n")

    # Here we ask customer for how many memebers they need room
    persons = input("Enter number of members who want to stay or press 0 to exit: ")

    # Here we verify the value entered by user is valid or not
    try:
        persons = int(persons)
        if persons == 0:
            # This condition took user to exit as user want exit 
            print("\nOperation aborted successfully")
            main_function()
        elif persons>0:
            # This condition procceed furthe process
            pass
        else:
            # This condition took user to exit as he put some invalid data
            print("\nPlease enter valid number")
            checkin_entery()
    except:
        print("\nPlease enter valid number")
        checkin_entery()

    # Here we fetch data for user as per customer choice
    mysql_crsr.execute(f"select * from Room_Records where Capacity>={persons} and Status='Free';")
    avilabe_rooms = mysql_crsr.fetchall()

    # This check is room avilabe or not as per customers condition
    if avilabe_rooms == []:
        print(f'\nNo single room avialabe for {persons} members\nKindly take rooms in smaller groups')
        checkin_entery()
    else:
        # In this case we show avilabe rooms to user
        avlb_r_table = pd.DataFrame(avilabe_rooms, columns=['Room_No', 'Capacity', 'Room_Type', 'Minimum_ChargeX24', 'Status'])
        print("\nAvilable Room Records....\n")
        print(avlb_r_table)

    # Here we make a list of avilabe rooms 
    avlb_r_list = []
    i = 0
    while i<len(avilabe_rooms):
        avlb_r_list.append(avilabe_rooms[i][0])
        i = i+1

    # Here user alots the room to his/her customer
    room_no = input("\nEnter room number from above table which you want to give to customer or enter 0 to exit: ")
    
    # Here we verifies, is user entered correct value or not
    try:
        room_no = int(room_no)
        if room_no == 0:
            print("\nProcess aborted successfully")
            main_function()
        elif room_no in avlb_r_list:
            # As user's value is in list so here we procced further
            pass
        else:
            print("\nYou entered unavliable room number so check-in process is reseted")
            checkin_entery()
    except:
        print("\nYou entered something invalid.")
        main_function()

    # Here we show ccharges to user for his/her customer
    paid_amount = room_records[room_no-1][3]
    print(f"\nCustomer have to pay minimum charge of {paid_amount}rs, that is valid for 24 Hours")

    # Here we took user choice as his/her customer paid or not
    print("\n1. Amount Paid Successfully\n2. Cancel Transaction\n")
    choice = input("Enter number of your choice: ")

    # It verifies that customerpaid or not
    if choice == '1':
        pass
    elif choice == '2':
        print("\nTransaction cancelled sucessfully")
        main_function()
    else:
        print("\nYou entered something invalid, so operation is cancelled")
        main_function()

    # Here we genrate necesarry values
    checkin_time = datetime.now()
    customer_no = customer_records[-1][0] + 1
    
    # Here we ask user for customer details
    name = input("Enter name of customer: ")
    contact_no = input("Enter customer contact number: ")
    customer_id = input("Enter verifiable customer ID name: ")
    id_number = input("Enter customer ID number: ")
    
    # Here we inserted and updated the data in MySQL database server 
    inserting_str = f"insert into Customer_Records values({customer_no}, '{name}', '{contact_no}', '{customer_id}', '{id_number}','{checkin_time}', '0000-00-00 00:00:00', {persons}, {room_no},{paid_amount},0,'Staying');"
    print(inserting_str)
    mysql_crsr.execute(inserting_str)
    mysql_crsr.execute(f"update room_records set Status ='Booked' where Room_No ={room_no};")
    mysql_obj.commit()  

    #Lending Slip Genration in PDF Format
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial" ,size=20)

    # This cell method will create the line in pdf page
    pdf.cell(0,25,"THE MANGEMENT HOTEL", ln=1, align="C")
    pdf.cell(0,4,"Hotel Staying Recipt", ln=1, align="C")
    pdf.set_font("Arial","B" ,size=18)
    pdf.cell(0,40,f"Customer Number : {customer_no}",ln=1,align="L")

    # This code changes the font aspects from here that will we written in PDF
    pdf.set_font("Arial", size=16)
    pdf.cell(0,0,f"Customer Name : {name}",ln=0,align="L") 
    pdf.cell(0,0,f"Check-in Date : {datetime.strftime(checkin_time,'%d-%m-%y')}",ln=1,align="R")
    pdf.cell(0,20,f"Customer Contact Number : {contact_no}",ln=0,align="L")  
    pdf.cell(0,20,f"Check-in Time : {datetime.strftime(checkin_time,'%H:%M:%S')}",ln=1,align="R")
    pdf.cell(0,0,f"Room Number : {room_no}",ln=1,align="L")
    pdf.cell(0,20,f"Members : {persons}",ln=1,align="L")
    pdf.cell(0,0,f"Paid Amount : {paid_amount}",ln=1,align="L")
    pdf.set_font("Arial","B" ,size=10)
    pdf.cell(0,20,"*This paid amount is minimum charge that is only for 24 hours next to check-in time",ln=1,align="L")
    pdf.cell(0,70,f"* Customer have to take care of this slip and it is necessary to bring this slip during checkout",ln=1,align="L")

    # This code make a pdf in the same loaction of program 
    pdf.output(f"Hotel_slip{customer_no}.pdf")

    # This code access the pdf file in computer location that we made above and open it
    os.startfile(f"Hotel_slip{customer_no}.pdf")

    fetch_mysql()
    main_function()

# This is sub-function of main function which runs on main function call, here we define functionality that will do the  i.e. updating the checkout in mysql records - 4th
def checkout_entery():
    print("\nHotel Check Out Entery....")
    # We took the user choice
    customer_no = input('\nEnter customer number from customer slip or enter 0 to cancel: ')
    # We verifies the user choice is integer or not
    try:
        customer_no = int(customer_no)
    except:
        print("\nPlease enter valid customer number")
        checkout_entery()
    if customer_no == 0:
        # This condition will check user want to cancel and pass if he/she entered correct value or not except 0
        print("\nChech-out operation cancelled successfully\n")
        main_function()
    elif customer_no in list(range(1,len(customer_records)+1)) and customer_records[customer_no-1][-1] == 'Staying':
        # This will calculate the styaing of customer
        entery_time = customer_records[customer_no-1][5]
        exit_time = datetime.now()
        staying_time = exit_time - entery_time
        staying_time = staying_time.days
        
        # This loop is for the persons who checkout the same day
        if staying_time == 0:
            staying_time = staying_time + 1
        else:
            # This condition will procedd further
            pass

        # Here we got the negative so by this we made it negative
        staying_days = abs(staying_time)

        # This will calculate the charges for customer
        mini_amount = customer_records[customer_no-1][-3]
        pay_amount = customer_records[customer_no-1][-3]*abs(staying_time)
        left_amount = pay_amount - mini_amount

        # Here we notify user, how much he should charge his customer
        print(f"\nCustomer payed {mini_amount}rs, now he/she have to pay {left_amount}rs\nThis charge is for {staying_days} day/s")
        
        # Here we took user choice as customer paid or not
        choice = input("\nPut 1 or 0 to procced or cancel respectively and press enter: ")
        if choice == '1':
            # This condition proceed us further
            pass
        elif choice == '0':
            # As user want to exit, we break this here and this will take us to main program
            print("\nChech-out operation aborted successfully\n")
            main_function()
        else:
            # As user entered invalid value, so we break this here and this will take us to main program
            print("\nYou entered invalid value, so operation is canceled.")
            main_function()

        # This condition will update the mysql enteries
        room_no = customer_records[customer_no-1][-4]
        # Quantity = lending_data[customer_no-1][-2] + equipments_data[item_id-1][-1]
        mysql_crsr.execute(f"update room_records set Status = 'Free' where Room_No = {room_no};")
        mysql_crsr.execute(f"update customer_records set Status = 'Left' where customer_no = {customer_no};")
        mysql_crsr.execute(f"update customer_records set Checkout_Time = '{datetime.now()}' where customer_no = {customer_no};")
        mysql_obj.commit()
        print("\nCustomer checkout successfully.\n")
    else:
        # Here user insert that value which is not in data
        print("\nPlease enter valid customer no.\n")
        checkout_entery()

    fetch_mysql()
    main_function()

def graphical_analysis():
    print('\nDay-wise earning analysis : \n')

    # Here we extract data from mysql which will be shown graphically
    mysql_crsr.execute("select sum(Paid_Amount),date(checkin_time) from customer_records group by date(checkin_time);")
    graph_data = mysql_crsr.fetchall()

    # Here we put this data into list form so that we can make graph from them
    x_items = []
    y_items = []
    day_numbers = []
    for i in range(len(graph_data)):
        x_items.append(int(graph_data[i][0]))
        y_items.append(calendar.day_name[datetime.weekday(graph_data[i][1])])
        day_numbers.append(datetime.weekday(graph_data[i][1]))
    
    # Here we arranged the data in proper way
    statstics_table = pd.DataFrame({'Day_Number':day_numbers,'Day':y_items, 'Earning':x_items,})
    statstics_table = statstics_table.sort_values('Day_Number')
    statstics_table = statstics_table.iloc[0:,1:]
    statstics_table = statstics_table.groupby('Day').sum()
    statstics_table = pd.DataFrame({'Day':list(statstics_table.index), 'Earning':list(statstics_table['Earning']),})

    # Here we show analysis in tabular form
    print(statstics_table)

    # here we plot the graph
    plt.bar(statstics_table['Day'],statstics_table['Earning'])
    plt.xlabel("Days")
    plt.ylabel("Earning(Rs)")
    plt.title("Day Wise Earning")

    #Here we show analysis in graphical form 
    plt.show()

    main_function()

#We define this main function that runs the whole program expect connectivity code
# In this we simply used a conditional loop that runs our program as per user choice
# In this conditional loop we recalls the sub functions as per user's choice
def main_function():
    print("\n1. View Room Records\n2. View Customer Records\n3. Entery for Customer Checkin\n4. Entery for Customer Checkout\n5. Earning Analysis\n0. Quit")
    choice = input("\nEnter your choice : ")
    if choice == '0':
        print('Shuting Down...')
        time.sleep(1)
    elif choice == '1':
        view_rooms()
    elif choice == '2':
        customer_data()
    elif choice == '3':
        checkin_entery()
    elif choice == '4':
        checkout_entery()
    elif choice == '5':
        graphical_analysis()
    else:
        print("\nPlease enter valid number\n")
        main_function()

# Here we welcome the user in our program and calls the main function
print("\nWelcome to Hotel Management\n")
main_function()