#!/usr/bin/env python
# coding: utf-8

# In[27]:


from tkinter import *
from tkinter import ttk
from Backend import *
from tkinter import messagebox

class Operator :
    def __init__(self,window):
        self.window = window
        self.op_login()
        
        
        
    def op_login(self):
        #new_window=Toplevel(self.window)
        self.window.title("Hello Operator")
        self.window.geometry("768x1024")
        
        button1=Button(self.window,text="Track Bikes",command=self.track_bikes)
        button1.place(x=40,y=40,width=120,height=25)
        button2=Button(self.window,text="Repair Bikes",command=self.repair_bike)
        button2.place(x=40,y=100,width=150,height=25)
        button3=Button(self.window,text="Move Bikes",command=self.move_bike)
        button3.place(x=40,y=160,width=120,height=25)
    
    def track_bikes(self):  
        a = Backend()
        self.new_window1=Toplevel(self.window)
        table = ttk.Treeview(self.new_window1, selectmode ='browse')
        
        def Trackme():
            if self.tkvar1.get() == "" :
                city_ = "all"
            else :
                city_ = int(self.tkvar1.get().split(' ',1)[0])
            
            if self.tkvar.get() == "" :
                loc_ = "all"
            else :
                loc_ = int(self.tkvar.get().split(' ',1)[0])            
            value=a.TrackBikes(loc_, city_)
            #bycicle_id, location_id, location_name , city_id, city_name , is_defective , is_rent,is_repaired
            #cols = ('Bicycle Id', 'Location Name','City Name', 'Is defective' , 'Is Rented' , 'Is Repaired')
          
            col_idx = ('1','2','3','4','5','6')
            cols = ('Bicycle Id', 'Location Name','City Name', 'Is defective' , 'Is Rented' , 'Is Repaired')
            # clear table content
            table.delete(*table.get_children())
            
            table.pack(side ='left') 
            table["columns"] = col_idx 
            table['show'] = 'headings'
            i = 0
            for c in col_idx :
                table.heading(c, text = cols[i])
                if i == 0 :
                    table.column(c, width = 100, anchor ='c' ) 
                else :
                    table.column(c, width = 100, anchor ='se' )  
                i += 1            
            for row in value :               
                table.insert("", 'end', values = (row[0],row[2], row[4] , ("Yes" if row[5]==1 else "No") , "Yes" if row[6]==1 else "No", "Yes" if row[7]==1 else "No")) 
         
        
        city_ , loc_ , choices_loc = "","", [] # selected city and loc declaration
        
        self.new_window1.title("Hello Operator-Track the bikes")
        self.new_window1.geometry("768x1024")
        label1=Label(self.new_window1,text="Enter City")
        label1.place(x=20,y=20)
        label2=Label(self.new_window1,text="Enter Location")
        label2.place(x=20,y=50)
        
        button=Button(self.new_window1,text="Track",command=Trackme)
        button.place(x=50,y=90,width=120,height=25)    
        
        self.tkvar1=StringVar(self.new_window1) # city option
        
        self.tkvar=StringVar(self.new_window1)    # loc option
        choices_loc= {'Choose city'}
        popupMenu1=OptionMenu(self.new_window1,self.tkvar,*choices_loc) 
        # city filter
        
        cities = a.getCities()
        
        choices_city = [(str(tups[0])+" "+tups[1]) for tups in cities]
        
        popupMenu=OptionMenu(self.new_window1,self.tkvar1,*choices_city)
        popupMenu.place(x=170, y=20,width=200,height=25)    
        def change_dropdown1(*args):
            city_ = self.tkvar1.get().split(' ',1)[0] # to get selected city, have to be splitted because optionmenu has no value and text at once
            locs = a.getLocations(city_id = city_) # get locations by city
            choices_loc = [(str(tups[0])+" "+tups[1]) for tups in locs]
            menu = popupMenu1['menu']
            menu.delete(0, 'end')
            for c in choices_loc:
                menu.add_command(label=c, 
                                 command=lambda value=c:
                                      self.tkvar.set(value))
    
        self.tkvar1.trace('w',change_dropdown1)
        
        # location filter     
        
        self.tkvar.set('')       
        popupMenu1.place(x=170, y=50,width=200,height=25)   
        def change_dropdown(*args):
            loc_ = self.tkvar.get().split(' ',1)[0]
            #print(tkvar.get())  
        self.tkvar.trace('w',change_dropdown)
      
        
      
        
    def repair_bike(self): 
        
        def updatebike():
            
            b = Backend()
            bycicle_id=tb1.get()
            Value = b.RepairBike(bycicle_id)
            if Value==True:
                messagebox.showinfo("Info","Bike has been repaired")
            else:
                messagebox.showinfo("Info","Bike has not been repaired")
                
        def Clear_repairbike():
            
            tb1.delete(0,"end")
            tb1.focus()
            
        new_window2=Toplevel(self.window)
        new_window2.title("Hello Operator-Repair the bikes")
        new_window2.geometry("450x200")
        label1=Label(new_window2,text="Enter Bike ID")
        label1.place(x=20,y=20)  
        tb1=Entry(new_window2,text= "")
        tb1.place(x=170, y=20,width=200,height=25)
        tb1["justify"]="left"
        tb1.focus() 
        button=Button(new_window2,text="Update",command=updatebike)
        button.place(x=50,y=90,width=120,height=25)
        button=Button(new_window2,text="Clear",command=Clear_repairbike)
        button.place(x=200,y=90,width=120,height=25)
        
    def move_bike(self):
        a = Backend()
        city_ , loc_ , choices_loc = "","", []
        def Move():
            bikeid=tbox1.get()
            if self.loc_opt.get() == "" :
                messagebox.showinfo("Info","Please select location first!")
            else :
                locid = int(self.loc_opt.get().split(" ")[0])
                
            
                output=a.MoveBike(bikeid,locid,0,0)
                if output==True:
                    messagebox.showinfo("Info","Bike has been moved successfully")
                else:
                    messagebox.showinfo("Info","Bike has been not moved.. Try Again!")
            
        
        def Clear_movebike():
            tbox1.delete(0,"end")
            tbox1.focus()
            
        new_window3=Toplevel(self.window)
        new_window3.title("Hello Operator-Keep moving the bikes")
        new_window3.geometry("768x1024")
        label1=Label(new_window3,text="Enter Bike ID")
        label1.place(x=20,y=20)
        label3=Label(new_window3,text="Enter new City")
        label3.place(x=20,y=80)
        label4=Label(new_window3,text="Enter new Location")
        label4.place(x=20,y=120)
        
        tbox1=Entry(new_window3,text= "")
        tbox1.place(x=170, y=20,width=200,height=25)
        tbox1["justify"]="left"
        tbox1.focus()
        
        
        self.city_opt=StringVar(new_window3) # city option
        self.loc_opt=StringVar(new_window3)    # loc option
        
        button=Button(new_window3,text="Move",command=Move)
        button.place(x=50,y=200,width=120,height=25)
        button=Button(new_window3,text="Clear",command=Clear_movebike)
        button.place(x=200,y=200,width=120,height=25)
        
        
        
        choices_loc= {'Choose Location'}
        popupMenu1=OptionMenu(new_window3,self.loc_opt,*choices_loc) 
        # city filter
        
        cities = a.getCities()
        choices_city = [(str(tups[0])+" "+tups[1]) for tups in cities]
        
        popupMenu=OptionMenu(new_window3,self.city_opt,*choices_city)
        popupMenu.place(x=170, y=80,width=200,height=25)    
        def change_dropdown1(*args):
            city_ = self.city_opt.get().split(' ',1)[0] # to get selected city, have to be splitted because optionmenu has no value and text at once
            locs = a.getLocations(city_id = city_) # get locations by city
            choices_loc = [(str(tups[0])+" "+tups[1]) for tups in locs]
            menu = popupMenu1['menu']
            menu.delete(0, 'end')
            for c in choices_loc:
                menu.add_command(label=c, 
                                 command=lambda value=c:
                                      self.loc_opt.set(value))
    
        self.city_opt.trace('w',change_dropdown1)
        
        # location filter     
        
        self.loc_opt.set('')       
        popupMenu1.place(x=170, y=120,width=200,height=25)   
        def change_dropdown(*args):
            loc_ = self.loc_opt.get().split(' ',1)[0]
            #print(self.tkvar.get())  
        self.loc_opt.trace('w',change_dropdown)
        
      



# In[ ]:





# In[ ]:




