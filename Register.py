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
from Customer import *
from Manager import *
from PIL import ImageTk
from PIL import Image
from win32api import GetSystemMetrics
class Register:
    def __init__(self,window):
        self.window=window
        self.window.wm_attributes('-alpha', 1) 
        self.window.title=("Login")
        self.window.geometry("1200x600+0+0")
        #self.window.resizable(False,False)
        
        self.image=Image.open("gemma-evans-ZDD9vLxqGqY-unsplash.jpg").resize((1280,720))
        self.logo=ImageTk.PhotoImage(self.image,master=self.window)
        print("Width =", GetSystemMetrics(0))
        print("Height =", GetSystemMetrics(1))
       
        
        self.photo_logo=Label(self.window,image=self.logo)
        self.photo_logo.place(x=0,y=0,width=1280,height=720)
        self.user_logo=ImageTk.PhotoImage(file="OIP.jpg", master=self.window)
        self.password_logo=ImageTk.PhotoImage(file="password.png", master=self.window)
        self.phoneno_logo=ImageTk.PhotoImage(file="phoneno.jpg", master=self.window)
        Frame_log=Frame(self.window,bg="white",)
        Frame_log.grid(sticky='we')
        Frame_log.place(x=450,y=180,height=450,width=360)
    
        username=Label(Frame_log,text="Username",bd=0,image=self.user_logo,compound=LEFT,font=("Goudy old style",15,"bold")
                        ,fg="black",bg="white")
        username.place(x=60,y=50)
        self.txt_user=Entry(Frame_log,bd=0, font=("Times new Roman",15),bg="lightgrey")
        self.txt_user.place(x=60,y=80,width=250)
        #self.txt_user.insert(0,"username")
        name=Label(Frame_log,text="Enter your Name",bd=0,image=self.user_logo,compound=LEFT,font=("Goudy old style",15,"bold")
                        ,fg="black",bg="white")
        name.place(x=60,y=130)
        self.txt_name=Entry(Frame_log,bd=0, font=("Times new Roman",15),bg="lightgrey")
        self.txt_name.place(x=60,y=160,width=250)
        Password=Label(Frame_log,text="Password",image=self.password_logo,compound=LEFT,font=("Goudy old style",15,"bold")
                        ,fg="black",bg="white").place(x=60,y=210)
        self.txt_pass=Entry(Frame_log,bd=0,show="*", font=("Times new Roman",15),bg="lightgrey")
        self.txt_pass.place(x=60,y=240,width=250)
        phoneno=Label(Frame_log,text="Enter your Phone no. ",bd=0,image=self.phoneno_logo,compound=LEFT,font=("Goudy old style",15,"bold")
                        ,fg="black",bg="white")
        phoneno.place(x=60,y=290)
        self.txt_phoneno=Entry(Frame_log,bd=0, font=("Times new Roman",15),bg="lightgrey")
        self.txt_phoneno.place(x=60,y=320,width=250)
        submit=Button(Frame_log,relief=FLAT,command=self.signup,text="Register",activebackground="#00B0F0",activeforeground="white",bg="DarkSeaGreen3",fg="#F0F8FF",font=("Arial",15)).place(x=60,y=350,width=250,)
        #Back_to_login=Button(Frame_log,relief=FLAT,command=self.login,text="Login",activebackground="#00B0F0",activeforeground="white",bg="DarkSeaGreen3",fg="#F0F8FF",font=("Arial",15)).place(x=250,y=380,width=50,)
    
    def signup(self):
        if self.txt_pass.get()=="" or self.txt_user.get()=="" or self.txt_name.get()=="" or self.txt_phoneno.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.window)
        else:
            obj=Backend()
            Val=[]
            val=(obj.AddCustomer(self.txt_user.get(),self.txt_name.get(),self.txt_pass.get(),self.txt_phoneno.get()))
            if val[0]:
                messagebox.showinfo("Info","You have been successfully registered",parent=self.window)
                self.window.withdraw()
            else :
                messagebox.showerror("Error",val[1],parent=self.window)
        
     
        
#window=Tk()

#obj=Register(window)
#window.mainloop()
