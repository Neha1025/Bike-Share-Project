# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 17:16:30 2021

@author: Annu Kajla
"""

from tkinter import *
from tkinter import ttk
import tkinter as tk
from Backend import *
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image
from datetime import datetime
class Customer():
    def __init__(self,window, cust_id ):         
        self.rent_id = []
        self.cust_id = cust_id
        self.window=window
        self.window.geometry("1300x800")        
        #my_menu=Menu(window)
        #window.config(menu=my_menu)
        self.window.configure(bg="white")
        self.window.wm_attributes('-alpha', 1) 
        white = "white"
        lavender = "lavender"
        
        self.style = ttk.Style(self.window)
        
        self.style.theme_create("yiil", parent='alt', settings={
                "TNotebook": {"configure": {"tabmargins": [5, 10, 2, 0] } },
                "TNotebook.Tab": {
                    "configure": {"padding": [5, 1], "background": white,"foreground":"black"},
                    "map":       {"background": [("selected", lavender)],
                                  "expand": [("selected", [1, 1, 1, 0])] } } } )
        
        self.style.theme_use("yiil")
        
        ##
        self.my_notebook=ttk.Notebook(self.window)
        self.my_notebook.pack()
        
        self.style.configure("TNotebook", background="white");
        #create all tab frames
        self.home_Frame=Frame(self.my_notebook)
        self.Rent_bike_frame=Frame(self.my_notebook,bg="light grey")
        self.Return_bike_Frame=Frame(self.my_notebook,bg="light grey")
        self.pay_bike_Frame=Frame(self.my_notebook,bg="light grey")
        #pack them
        self.home_Frame.pack(fill="both",expand=1)
        self.Rent_bike_frame.pack(fill="both",expand=1,ipadx=40)
        self.Return_bike_Frame.pack(fill="both",expand=1)

        #add tabs to the notebook
        self.my_notebook.add(self.home_Frame,text="Home")
        self.my_notebook.pack(expand=1,fill='both')
        self.my_notebook.add(self.Rent_bike_frame,text="Rent Bike")
        self.my_notebook.add(self.Return_bike_Frame,text="Return Bike")     
               
        self.image=Image.open("daniel-salcius-RRcYcdGY630-unsplash.jpg").resize((1280,720))
        self.logo=ImageTk.PhotoImage(self.image, master = self.window)
        photo_logo=Label(self.home_Frame,image = self.logo)
        photo_logo.place(x=0,y=0,width=1280,height=720)
    
        
        self.photo_logo=Label(self.Rent_bike_frame,image=self.logo)
        self.photo_logo.place(x=0,y=0,width=1280,height=720)
        
        self.photo_logo=Label(self.Return_bike_Frame,image=self.logo)
        self.photo_logo.place(x=0,y=0,width=1280,height=720)
        
        self.home()
        self.Book_ride()
        self.return_bike()
    
    #create home page function
    
    def home(self):
         
         msg=Label(self.home_Frame,text="Rido-RIDE WITH  US",bg="azure2",font=('times', 24, 'italic'))
         msg.place(x=60,y=300)
         description=Label(self.home_Frame,text="Rido is on a mission of making daily commute stress-free, time-saving, reliable and convenient."+"\n"+"Rido provides hassle free bike bookings supported in multiple cities and various locations",bg="azure2",bd=0,font=("times",14))
         description.place(x=60,y=390)
        
       #  bookRide=Button(Welcome_msg,text="Book your ride here now",command=Book_ride)
        # bookRide.grid(column=0,row=1,sticky='W')
    def Book_ride(self):
        def book():
            book_obj=Backend()
            bicycle_ID=bicycleID.get()
            list_bikes = book_obj.getBikes(id = bicycle_ID,is_defective=0, is_rent=0,
                 is_repaired = 0)
            print (list_bikes)
            if list_bikes == [] :
                messagebox.showinfo("Info","No Available Bicycle with ID "+bicycle_ID)
            else :
                list1=[]
                #cust_id=CustomerID.get()
                start_id=startId.get()            
                #StartTime=Start_Time.get()
                location_start_Id=location_startId.get().split(" ")[0]            
                list1=(book_obj.AddBikeRent(int(self.cust_id),int(bicycle_ID),int(location_start_Id),start_id))            
                messagebox.showinfo("Info","Your rent ID has been generated successfully: "+list1[1])
            
        
        Book_frame=LabelFrame(self.Rent_bike_frame,bg="light grey",text="Book your ride now")
        Book_frame.grid(column=0,row=0,padx=500,pady=120)
        
        CustomerID_label=Label(Book_frame,text="Customer Id:",bd=0,bg="light grey")
        CustomerID_label.grid(column=0,row=1,sticky='W',padx=8,pady=7)
        CustomerID=Label(Book_frame, text = self.cust_id , font = "Arial 12 bold",bd=0,bg="light grey") # default by Login
        CustomerID.grid(row = 1,column = 1,padx=15)
        
        startId_Label=Label(Book_frame,text="Enter your start time:",bg="light grey")
        startId_Label.grid(column=0,row=2,sticky='W',pady=7,padx=8)
        startId = Entry(Book_frame)        
        start_ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        startId.insert(END, start_) # set date time by default (current time)
        startId.config(state = "readonly")
        startId.grid(row = 2,column = 1)
        bicycleID_label=Label(Book_frame,text="Bicycle Id:",bg="light grey")
        bicycleID_label.grid(column=0,row=3,sticky='W',padx=8,pady=7)
        bicycleID = Entry(Book_frame)
        bicycleID.grid(row = 3,column = 1,padx=15)
        
        # dropdown location
        location_startId_Label=Label(Book_frame,text="Enter your location start id:",bg="light grey")
        location_startId_Label.grid(column=0,row=4,sticky='W',pady=7,padx=8)
        a = Backend()
        locs = a.getLocations()
        choices_loc = [(str(i[0])+" "+i[1]+" "+i[3]) for i in locs]
        location_startId=StringVar(Book_frame)
        popupMenu=OptionMenu(Book_frame,location_startId,*choices_loc) 
        popupMenu.grid(row = 4,column = 1)
       
        #location_startId = Entry(Book_frame)
        #location_startId.grid(row = 4,column = 1)
        
        submit=Button(Book_frame,relief=FLAT,command=book,text="Submit",activebackground="#00B0F0",activeforeground="white",bg="DarkSeaGreen3",fg="#F0F8FF",font=("Arial",10)).grid(column=0,row=5,sticky='W',padx=7,pady=7)
    
    
    #Return a bike
    def return_bike(self):
        Obj=Backend()
        
        def pay():
            rent=RentID.get()
            r = Obj.GetRentById(int(rent))
            print (r)
            if r[0][13] == None or r[0][13] == "" or r[0][13] == 0 : # column 'paid'                                
                #Locid=LocationendID.get()
                Locid=LocationendID.get().split(" ")[0]
                endtime=End_Time.get()
                val=[]
                val= Obj.ReturnBike(int(rent),int(Locid),endtime)
                value=[]
                value=Obj.GetCharge(int(rent))
                
                print(value) 
                
                def paid():
                     #rid=Rent_ID.get()
                     rid = rent
                     P=Paid_date.get()
                     Answer=Obj.PayCharge(int(rent),value,P)    
                     #print("Payment is :",Answer)
                     messagebox.showinfo("Info","Payment is :" + Answer[1])
               
                window2=Toplevel(self.window)
                #window2=Tk(self)             
                window2.geometry("1300x800")
                self.pay_bike_Frame=Frame(window2,bg="light grey")
                self.pay_bike_Frame.pack(fill="both",expand=1)
                pay_frame=LabelFrame(self.pay_bike_Frame,bg="light grey",text="Please Pay for your ride : £ %.2f" % (value))
                pay_frame.grid(column=0,row=0,padx=500,pady=120)
                RentID_label=Label(pay_frame,text="Rent Id:",bd=0)
                RentID_label.grid(column=0,row=1,sticky='W',padx=8,pady=7)
                #Rent_ID = Entry(pay_frame)
                Rent_ID=Label(pay_frame,text=rent,bd=0, font = "Arial 10 bold") # default by previous windows
                Rent_ID.grid(row = 1,column =1,padx=15)
                Paid_date_label=Label(pay_frame,text="Paid date:")
                Paid_date_label.grid(column=0,row=2,sticky='W',padx=8,pady=7)
                Paid_date = Entry(pay_frame)
                pd_ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Paid_date.insert(END, pd_) # set date time by default (current time)
                Paid_date.config(state = "readonly")
                Paid_date.grid(row = 2,column = 1,padx=15)
                Pay=Button(pay_frame,relief=FLAT,command=paid,text="Submit",activebackground="#00B0F0",activeforeground="white",bg="DarkSeaGreen3",fg="#F0F8FF",font=("Arial",10)).grid(column=0,row=5,sticky='W',padx=7,pady=7)
            else :
                messagebox.showinfo("Info","Rent ID %s is already over. The bike was returned." % (rent))
        
        def report():
             def Reportbike():
                  bid= BicycleID.get()
                  vari=Obj.ReportBike(int(bid))
                  if vari:
                      messagebox.showinfo("Info","Bike has been reported")
                  else:
                       messagebox.showerror("Error","Try Again!!")
             #window3=Tk()
             window3=Toplevel(self.window)
             window3.geometry("500x500+100+100")
             report_bike_Frame=Frame(window3,bg="light grey")
             report_bike_Frame.pack(fill="both",expand=1)
             report_frame=LabelFrame(report_bike_Frame,bg="light grey",text="Please report the bike")
             report_frame.grid(column=0,row=0,padx=500,pady=120)
             Bicycle_id_label=Label(report_frame,text="bicycle Id:",bd=0)
             Bicycle_id_label.grid(column=0,row=1,sticky='W',padx=8,pady=7)
             BicycleID = Entry(report_frame)
             BicycleID.grid(row = 1,column =1,padx=15)
             report_bi=Button(report_frame,text="Report",command=Reportbike,bg="light grey",fg="#d77337",bd=0,font=("times new roman",12)).grid(column=0,row=3,sticky='W')
        
        
        Return_frame=LabelFrame(self.Return_bike_Frame,bg="light grey",text="Return Bike")
        Rents_Frame=LabelFrame(self.Return_bike_Frame,bg="light grey",text="Your Rent :")
        #Return_frame.grid(column=1,row=0,padx=500,pady=120)
        Return_frame.grid(column=1,row=0,padx=50,pady=50)
        Rents_Frame.grid(column=0,row=0,padx=50,pady=50)
        
        
        #show list rent of this customer
        rents = Obj.GetRentByCust(self.cust_id)
        table = ttk.Treeview(Rents_Frame, selectmode ='browse')
        # clear table content
        col_idx = ('1','2','3','4','5')
        #rent_id, customer_id,customer_name, bycicle_id, location_start_name, city_start,   start_time
        cols = ('Rent ID', 'Customer Name', "Bicycle ID", "Location Start", "Start Time")
        table.delete(*table.get_children())        
        table.pack(fill ='x') 
        table["columns"] = col_idx 
        table['show'] = 'headings'
        i = 0
        for c in col_idx :
            table.heading(c, text = cols[i])
            if i == 0 or i == 2:
                table.column(c, width = 50, anchor ='c' ) 
            else :
                table.column(c, width = 150, anchor ='c' )  
            i += 1            
        for row in rents :               
            table.insert("", 'end', values = (row[0],row[2], row[3] ,row[4] + " " +row[5],row[6] ))
        
        RentID_label=Label(Return_frame,text="Rent Id:",bd=0)
        RentID_label.grid(column=0,row=1,sticky='W',padx=8,pady=7)
        RentID = Entry(Return_frame)
       
        RentID.grid(row = 1,column = 1,padx=15)
        Location_endID_label=Label(Return_frame,text="Location end Id:")
        Location_endID_label.grid(column=0,row=3,sticky='W',padx=8,pady=7)
         # dropdown location        
        a = Backend()
        locs = a.getLocations()
        choices_loc = [(str(i[0])+" "+i[1]+" "+i[3]) for i in locs]
        LocationendID=StringVar(Return_frame)
        popupMenu=OptionMenu(Return_frame,LocationendID,*choices_loc) 
        popupMenu.grid(row = 3,column = 1,padx=15)
        #LocationendID = Entry(Return_frame)
        #LocationendID.grid(row = 3,column = 1,padx=15)
        End_Time_Label=Label(Return_frame,text="Enter ride end time:")
        End_Time_Label.grid(column=0,row=4,sticky='W',pady=7,padx=8)
        End_Time= Entry(Return_frame)
        end_date_ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        End_Time.insert(END, end_date_) # set date time by default (current time)
        End_Time.config(state = "readonly")
        End_Time.grid(row = 4,column = 1)
        
        
        submit=Button(Return_frame,relief=FLAT,command=pay,text="Submit",activebackground="#00B0F0",activeforeground="white",bg="DarkSeaGreen3",fg="#F0F8FF",font=("Arial",10)).grid(column=0,row=5,sticky='W',padx=7,pady=7)
        reportBike=Button(Return_frame,text="Report Bike?",command=report,bg="light grey",fg="#d77337",bd=0,font=("times new roman",12)).grid(column=3,row=5,sticky='W')
        
        
        
        
        
            
#home()
#Book_ride()
#return_bike()

#window2.mainloop()
#window.mainloop()

