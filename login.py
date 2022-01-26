# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 15:14:18 2021

@author: Annu Kajla
"""
# =============================================================================
# import os
from tkinter import *
from tkinter import messagebox
from Backend import *
from Operator import *
from Manager import *
from Customer import *
from Register import *
from PIL import ImageTk
from PIL import Image

class Login:
    def __init__(self,window):
        self.window=window
        self.window.wm_attributes('-alpha', 1) 
        self.window.title=("Login")
        self.window.geometry("1200x600+0+0")
        #self.window.resizable(False,False)
        
        image=Image.open("gemma-evans-ZDD9vLxqGqY-unsplash.jpg").resize((1280,720))
        self.logo=ImageTk.PhotoImage(image)
               
        self.photo_logo=Label(self.window,image=self.logo)
        self.photo_logo.place(x=0,y=0,width=1280,height=720)
        self.user_logo=ImageTk.PhotoImage(file="OIP.jpg")
        self.password_logo=ImageTk.PhotoImage(file="password.png")
        Frame_log=Frame(self.window,bg="white",)
        Frame_log.grid(sticky='we')
        Frame_log.place(x=450,y=180,height=300,width=360)
    
        username=Label(Frame_log,text="Username",bd=0,image=self.user_logo,compound=LEFT,font=("Goudy old style",15,"bold")
                        ,fg="black",bg="white")
        username.place(x=50,y=50)
        self.txt_user=Entry(Frame_log,bd=0, font=("Times new Roman",15),bg="lightgrey")
        self.txt_user.place(x=50,y=80,width=250)
        #self.txt_user.insert(0,"username")
        Password=Label(Frame_log,text="Password",image=self.password_logo,compound=LEFT,font=("Goudy old style",15,"bold")
                        ,fg="black",bg="white").place(x=50,y=130)
        self.txt_pass=Entry(Frame_log,bd=0,show="*", font=("Times new Roman",15),bg="lightgrey")
        self.txt_pass.place(x=50,y=160,width=250)
        
        submit=Button(Frame_log,relief=FLAT,command=self.log,text="Login",activebackground="#00B0F0",activeforeground="white",bg="DarkSeaGreen3",fg="#F0F8FF",font=("Arial",15)).place(x=50,y=220,width=250,)
        
        register=Button(Frame_log,relief=FLAT,command=self.reg,text="Register",bg="white",fg="#d77337",bd=0,font=("times new roman",12)).place(x=250,y=260,width=50)
    def reg(self):
        #ob=Register(self.window,self)
        self.regWindow = Tk()
        op = Register(self.regWindow)
        
    def log(self):
        if self.txt_pass.get()=="" or self.txt_user.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.window)
        
        else:
            b = Backend()
            res = b.ValidateUser(self.txt_user.get(), self.txt_pass.get())
            if res[0] == False:
                messagebox.showinfo("welcome","User not found",parent=self.window)
            else :
                # 2-nd column is role_id
                if res[1] == 1: # show Customer GUI                     
                    self.window.withdraw()
                    self.newWindow = Tk()
                    cust_id = res[0]
                    op = Customer(self.newWindow, cust_id)
                elif res[1] == 2: # show Operator GUI 
                    self.window.withdraw()
                    self.newWindow = Tk()
                    op = Operator(self.newWindow)
                elif res[1] == 3: # show Manager GUI 
                    self.window.withdraw()
                    self.newWindow = Tk()
                    op = Manager(self.newWindow)
                else :
                    messagebox.showinfo("welcome","Role not registered",parent=self.window)
        
window=Tk()        
obj=Login(window)
window.mainloop()


