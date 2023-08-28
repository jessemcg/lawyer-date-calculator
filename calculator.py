#!/usr/bin/python3

# MIT License
#
# Copyright (c) 2023 Jesse McGowan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# SPDX-License-Identifier: MIT

import gi
from datetime import datetime, timedelta, date
from dateutil import relativedelta
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class LawyerDateCalculator(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Lawyer Date Calculator")
        self.set_border_width(9)

        # Connect the key-press-event to the appropriate handler
        self.connect("key-press-event", self.on_key_press_event)

        # Grid
        grid = Gtk.Grid()
        grid.set_column_spacing(15)  # Set the column spacing to 20 pixels
        grid.set_row_spacing(15)  # Set the row spacing to 20 pixels
        self.add(grid)

        # Due Date From Today
        self.duefromtoday_entry = Gtk.Entry()
        self.duefromtoday_entry.set_placeholder_text("#")
        self.duefromtoday_entry.set_width_chars(3)  # Set width to 10 characters
        box = Gtk.Box()
        box.pack_start(self.duefromtoday_entry, False, False, 0)
        box.set_halign(Gtk.Align.START)
        grid.attach(box, 0, 0, 1, 1)
        label_box = Gtk.Box()
        label_box.pack_start(Gtk.Label(label="Due Date From Today"), False, False, 0)
        label_box.set_halign(Gtk.Align.END)
        grid.attach(label_box, 1, 0, 2, 1)

        # Due Date From Diff Date
        self.startdate_entry = Gtk.Entry()
        self.startdate_entry.set_placeholder_text("mm/dd/yyyy")
        self.startdate_entry.set_width_chars(9)  # Set width to 15 characters
        box = Gtk.Box()
        box.pack_start(self.startdate_entry, False, False, 0)
        box.set_halign(Gtk.Align.START)
        grid.attach(box, 0, 1, 1, 1)
        self.daysadded_entry = Gtk.Entry()
        self.daysadded_entry.set_placeholder_text("#")
        self.daysadded_entry.set_width_chars(3)  # Set width to 5 characters
        box = Gtk.Box()
        box.pack_start(self.daysadded_entry, False, False, 0)
        box.set_halign(Gtk.Align.START)
        grid.attach(box, 1, 1, 1, 1)
        label_box = Gtk.Box()
        label_box.pack_start(Gtk.Label(label="Due Date From a Different Date"), False, False, 0)
        label_box.set_halign(Gtk.Align.END)
        grid.attach(label_box, 2, 1, 1, 1)

        # Age From DOB
        self.age_entry = Gtk.Entry()
        self.age_entry.set_placeholder_text("mm/dd/yyyy")
        self.age_entry.set_width_chars(9)  # Set width to 10 characters
        box = Gtk.Box()
        box.pack_start(self.age_entry, False, False, 0)
        box.set_halign(Gtk.Align.START)
        grid.attach(box, 0, 2, 1, 1)
        label_box = Gtk.Box()
        label_box.pack_start(Gtk.Label(label="Age Based on Date of Birth"), False, False, 0)
        label_box.set_halign(Gtk.Align.END)
        grid.attach(label_box, 1, 2, 2, 1)

        # Diff Between Two Dates
        self.firstdate_entry = Gtk.Entry()
        self.firstdate_entry.set_placeholder_text("mm/dd/yyyy")
        self.firstdate_entry.set_width_chars(9)  # Set width to 15 characters
        box = Gtk.Box()
        box.pack_start(self.firstdate_entry, False, False, 0)
        box.set_halign(Gtk.Align.START)
        grid.attach(box, 0, 3, 1, 1)
        self.seconddate_entry = Gtk.Entry()
        self.seconddate_entry.set_placeholder_text("mm/dd/yyyy")
        self.seconddate_entry.set_width_chars(9)  # Set width to 15 characters
        box = Gtk.Box()
        box.pack_start(self.seconddate_entry, False, False, 0)
        box.set_halign(Gtk.Align.START)
        grid.attach(box, 1, 3, 1, 1)
        label_box = Gtk.Box()
        label_box.pack_start(Gtk.Label(label="Difference Between Two Dates"), False, False, 0)
        label_box.set_halign(Gtk.Align.END)
        grid.attach(label_box, 2, 3, 1, 1)

        # Calculate button
        calculate_button = Gtk.Button(label="Calculate")
        calculate_button.connect("clicked", self.calculate)
        grid.attach(calculate_button, 0, 4, 3, 1)

        # Output label
        self.output_label = Gtk.Label(label="")
        grid.attach(self.output_label, 0, 5, 3, 1)

    def on_key_press_event(self, widget, event):
        # Check if the key pressed was the "Enter" key
        keyname = Gdk.keyval_name(event.keyval)
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
        if keyname == "Return" or keyname == "KP_Enter":
            self.calculate(widget)
        elif ctrl and keyname == "q":
            Gtk.main_quit()

    def calculate(self, widget):
        duefromtoday = self.duefromtoday_entry.get_text()
        startdate = self.startdate_entry.get_text()
        daysadded = self.daysadded_entry.get_text()
        age = self.age_entry.get_text()
        firstdate = self.firstdate_entry.get_text()
        seconddate = self.seconddate_entry.get_text()

        if duefromtoday:
            self.duefromtoday(duefromtoday)
        elif startdate and daysadded:
            self.duefromdiff(startdate, daysadded)
        elif age:
            self.age(age)
        elif firstdate and seconddate:
            self.diff(firstdate, seconddate)
        else:
            self.output_label.set_text("Please fill out the inputs")

    def duefromtoday(self, num1):
        num1 = int(num1)
        Begindate = date.today()
        Enddate = Begindate + timedelta(days=num1)
        Enddate_formatted = Enddate.strftime("%B %d, %Y")
        self.output_label.set_markup(f"<b>{Enddate_formatted}</b>")

    def duefromdiff(self, Begindatestring, num1):
        num1 = int(num1)
        Begindate = datetime.strptime(Begindatestring, "%m/%d/%Y")
        Enddate = Begindate + timedelta(days=num1)
        Enddate_formatted = Enddate.strftime("%B %d, %Y")
        self.output_label.set_markup(f"<b>{Enddate_formatted}</b>")

    def age(self, birthDate):
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
        self.output_label.set_markup(f"<b>{age}</b>")

    def diff(self, str_d1, str_d2):
        d1 = datetime.strptime(str_d1, "%m/%d/%Y")
        d2 = datetime.strptime(str_d2, "%m/%d/%Y")
        delta = relativedelta.relativedelta(d2, d1)
        self.output_label.set_markup(f"<b>{delta.years} years, {delta.months} months, and {delta.days} days</b>")
        
def run():
	win = LawyerDateCalculator()
	win.connect("destroy", Gtk.main_quit)
	win.show_all()
	Gtk.main()

