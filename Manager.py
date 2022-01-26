# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 12:00:14 2021

@author: ewanhilton
"""

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from tkinter import *
from tkinter import messagebox
import tkinter.font as font
from Backend import *

class Manager:
    def __init__(self,  window):
        self.window = window
        self.window.geometry("768x1024")
        self.window.title("Manager - Bike Rental Reports")
        self.labelselectreport = Label(text = "Select which report you want to view")
        self.labelerror = Label(window,text = "You must select a report!")
        OPTIONS = [
            "Please select",
            "Bike usage",
            "Bikes per location",
            "Profit per month"] 
            
        self.reports = StringVar(window)
        self.reports.set(OPTIONS[0]) 
           
        self.dropdown = OptionMenu(window, self.reports, *OPTIONS)
        self.dropdown["bg"] = "#fff"
        self.dropdown["menu"].config(bg="#fff")
            
        self.boldFont = font.Font(weight="bold")
        self.buttondisplay = Button(window,text = "Display", command = self.DisplayReport)
        self.buttondisplay["bg"] = "#4CAF50"
        self.buttondisplay["fg"] = "#fff"
        self.buttondisplay['font'] = self.boldFont
        fig = Figure(figsize=(10,10))
        self.canvas = FigureCanvasTkAgg(fig, master=self.window)

        self.labelselectreport.pack(side = TOP)
        self.dropdown.pack(side = TOP )
        self.buttondisplay.pack(side = TOP)
        
    def DisplayReport(self):
        selection = self.reports.get()
        try: 
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError: 
            pass 
        
        if selection =="Please select":
            self.labelerror = Label(text = "You must select a report!")
            self.labelerror["fg"] = "red"
            self.labelerror.pack()
            return
        elif selection == "Profit per month":
            self.DisplayProfits()
        elif selection =="Bike usage":          
            self.DisplayBikeUsage()
        elif selection =="Bikes per location":
            self.DisplayLocations()
        else:
            self.labelerror.pack_forget()
            
            
    def DisplayProfits(self):
        messagebox.showinfo("Not yet available","This feature is coming soon")
            
    def DisplayLocations(self):

        try:
            backend = Backend()
            location_names,counts = backend.GetBikeLocationInfo()      
            fig = Figure(figsize=(10,10))
            subplot = fig.add_subplot(111)
            subplot.bar(location_names, counts)
            subplot.set_title ("Bikes per location", fontsize=16)
            subplot.set_ylabel("Number of bikes", fontsize=14)
            subplot.set_xlabel("Location", fontsize=14)
            
            self.canvas = FigureCanvasTkAgg(fig, master=self.window)
            self.canvas.get_tk_widget().pack()
            self.canvas.draw()
        except Exception as ex:
            messagebox.showerror("Error","Something went wrong!\n" +str(ex))
        
    def DisplayBikeUsage(self):       

        try:        
            backend = Backend()
            labels,colors,values,explode = backend.GetBikeUsageInfo()          
            fig = Figure(figsize=(10,5))
            subplot = fig.add_subplot(111)
            subplot.pie(values, labels=labels,autopct='%.2f%%', explode=explode,shadow=True,colors=colors)
            self.canvas = FigureCanvasTkAgg(fig, master=self.window)
            self.canvas.get_tk_widget().pack()
            self.canvas.draw()
            
        except Exception as ex:
            messagebox.showerror("Error","Something went wrong!\n" +str(ex))

            

                    