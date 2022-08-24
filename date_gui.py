#!/usr/bin/python3

import PySimpleGUI as sg
from datetime import datetime
from datetime import timedelta
from datetime import date
from dateutil import relativedelta

# PysimpleGUI Layout
# Simple message at the top
layout = [  [sg.Text("date format = mm/dd/yyyy")], 
# Buttons and input boxes
            [sg.Button('Due Date from Today', size=(30,1)), sg.Text("adding"), sg.Input(size=(3,1), key='-duefromtoday_input-'), sg.Text("days")],
            [sg.Button('Due Date from Diff Date', size=(30,1)), sg.Text("start date"), sg.Input(size=(10,1), key='-startdate_input-'), sg.Text("adding"), sg.Input(size=(3,1), key='-daysadded_input-'),sg.Text("days")],
            [sg.Button('Calculate Age', size=(30,1)), sg.Text("date of birth"), sg.Input(size=(10,1), key='-age_input-')],
            [sg.Button('Diff Between Two Dates', size=(30,1)), sg.Text("first date"), sg.Input(size=(10,1), key='-firstdate_input-'), sg.Text("second date"), sg.Input(size=(10,1), key='-seconddate_input-')],
# Output message      
            [sg.Text(key='-OUTPUT-')]  ]

# Create the main window
window = sg.Window('Calculate Dates', layout, font="_")

# Functions to do the calculations

# Calculates due date from today
def duefromtoday():
    num1 = values['-duefromtoday_input-']
    num1 = int(num1)
    Begindate = date.today()
    Enddate = Begindate + timedelta(days=num1)
    Enddate_formatted = Enddate.strftime("%B %d, %Y") 
    values['-duedate-'] = Enddate_formatted
    return None

# Calculates due date from a different date
def duefromdiff():
    Begindatestring = values['-startdate_input-']
    num1 = values['-daysadded_input-']
    num1 = int(num1)
    Begindate = datetime.strptime(Begindatestring, "%m/%d/%Y")
    Enddate = Begindate + timedelta(days=num1)
    Enddate_formatted = Enddate.strftime("%B %d, %Y")
    values['-duedate-'] = Enddate_formatted
    return None

# Calculates someone age if date of birth provided
def age():
    birthDate = values['-age_input-']
    birthDate = datetime.strptime(birthDate, "%m/%d/%Y").date()
    currentDate = datetime.today().date()
    age = currentDate.year - birthDate.year
    monthVeri = currentDate.month - birthDate.month
    dateVeri = currentDate.day - birthDate.day
    age = int(age)
    monthVeri = int(monthVeri)
    dateVeri = int(dateVeri)
    if monthVeri < 0 :
        age = age-1
    elif dateVeri < 0 and monthVeri == 0:
        age = age-1
    values['-duedate-'] = age
    return None

# Calculates the time between two dates
def diff():
    str_d1 = values['-firstdate_input-']
    str_d2 = values['-seconddate_input-']
    d1 = datetime.strptime(str_d1, "%m/%d/%Y")
    d2 = datetime.strptime(str_d2, "%m/%d/%Y")
    delta = relativedelta.relativedelta(d2, d1)
    values['-duedate-'] = f"{delta.years} years, {delta.months} months, and {delta.days} days"
    return None
    
# Calling each function with an if statement tied to their pysimpple gui submit button
while True:
    event, values = window.read()
    if event == 'Due Date from Today':
        duefromtoday()
    if event == 'Due Date from Diff Date':
        duefromdiff()
    if event == 'Calculate Age':
        age()
    if event == 'Diff Between Two Dates':
        diff()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Close':
        break
    # Output the answer in large yellow font
    window['-OUTPUT-'].update(values['-duedate-'], text_color='yellow', font='Helvetica 16')
