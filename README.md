# lawyer-date-calculator
Simple date calculator for scheduling deadlines and the like. The month or day may be single digit, but the year must be four digits. The enter button can be used instead of the calculate button. This app is written in Python and has a GTK4 GUI. It only works on linux. Windows users can use [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install).

<img src="screenshot.png" width="690">

## Install

Install python datetuil module:

	pip install python-dateutil

Download the calculator

	git clone https://github.com/jessemcg/lawyer-date-calculator.git

Make sure it is executable:

	chmod +x $HOME/lawyer-date-calculator/LawyerDateCalculator.py
	
Run it from the terminal:

	python $HOME/lawyer-date-calculator/LawyerDateCalculator.py
	
Or place the above command in a script launching app like [Launcher](https://extensions.gnome.org/extension/5874/launcher/) or create a .desktop file for it with something like [Pin It](https://flathub.org/apps/com.github.ryonakano.pinit).

