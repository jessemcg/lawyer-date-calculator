#!/usr/bin/python3

import gi
from datetime import datetime, timedelta, date
from dateutil import relativedelta
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk

class LawyerDateCalculator(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Lawyer Date Calculator")

        # Grid
        grid = Gtk.Grid()
        grid.set_column_spacing(40)
        grid.set_row_spacing(15)
        grid.set_margin_top(30)
        grid.set_margin_bottom(15)
        grid.set_margin_start(20)
        grid.set_margin_end(20)
        
        # Set the grid as the child of the window
        self.set_child(grid)
        
        # Create a ShortcutController
        shortcut_controller = Gtk.ShortcutController.new()
        self.add_controller(shortcut_controller)

        # Create a shortcut for Control+Q
        key_combination = Gtk.ShortcutTrigger.parse_string("<Control>q")
        shortcut = Gtk.Shortcut.new(key_combination, Gtk.CallbackAction.new(self.quit_app))
        shortcut_controller.add_shortcut(shortcut)
        
        # Due Date From Today
        self.duefromtoday_entry = Gtk.Entry()
        self.duefromtoday_entry.set_placeholder_text("# of days")
        self.duefromtoday_entry.connect("activate", self.calculate)
        grid.attach(self.duefromtoday_entry, 0, 0, 1, 1)
        label = Gtk.Label(label="Due Date From Today")
        label.set_halign(Gtk.Align.END)
        grid.attach(label, 1, 0, 2, 1)

        # Due Date From Diff Date
        self.startdate_entry = Gtk.Entry()
        self.startdate_entry.set_placeholder_text("mm/dd/yyyy")
        grid.attach(self.startdate_entry, 0, 1, 1, 1)
        self.daysadded_entry = Gtk.Entry()
        self.daysadded_entry.set_placeholder_text("# of days")
        self.daysadded_entry.set_width_chars(3)
        self.daysadded_entry.connect("activate", self.calculate)
        grid.attach(self.daysadded_entry, 1, 1, 1, 1)
        label = Gtk.Label(label="Due Date From a Different Date")
        label.set_halign(Gtk.Align.END)
        grid.attach(label, 2, 1, 1, 1)

        # Age From DOB
        self.age_entry = Gtk.Entry()
        self.age_entry.set_placeholder_text("mm/dd/yyyy")
        self.age_entry.connect("activate", self.calculate)
        grid.attach(self.age_entry, 0, 2, 1, 1)
        label = Gtk.Label(label="Age Based on Date of Birth")
        label.set_halign(Gtk.Align.END)
        grid.attach(label, 1, 2, 2, 1)

        # Diff Between Two Dates
        self.firstdate_entry = Gtk.Entry()
        self.firstdate_entry.set_placeholder_text("mm/dd/yyyy")
        grid.attach(self.firstdate_entry, 0, 3, 1, 1)
        self.seconddate_entry = Gtk.Entry()
        self.seconddate_entry.set_placeholder_text("mm/dd/yyyy")
        self.seconddate_entry.connect("activate", self.calculate)
        grid.attach(self.seconddate_entry, 1, 3, 1, 1)
        label = Gtk.Label(label="Difference Between Two Dates")
        label.set_halign(Gtk.Align.END)
        grid.attach(label, 2, 3, 1, 1)

        # Calculate button
        calculate_button = Gtk.Button(label="Calculate")
        calculate_button.connect("clicked", self.calculate)
        grid.attach(calculate_button, 0, 4, 3, 1)

        # Output label
        self.output_label = Gtk.Label(label="")
        grid.attach(self.output_label, 0, 5, 3, 1)
        
        # Create an event controller for key presses
        key_controller = Gtk.EventControllerKey.new()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_controller)

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
        
    def on_key_pressed(self, controller, keyval, keycode, state):
        keyname = Gdk.keyval_name(keyval)
        if keyname == "Return" or keyname == "KP_Enter":
            self.calculate(None)

    def quit_app(self, *args):
        self.get_application().quit()
        
class LawyerDateCalculatorApp(Gtk.Application):
    def __init__(self):
        super().__init__()

    def do_activate(self):
        win = LawyerDateCalculator(self)
        win.present()  # Use present instead of show

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = LawyerDateCalculatorApp()
app.run(None)

        
        
        
