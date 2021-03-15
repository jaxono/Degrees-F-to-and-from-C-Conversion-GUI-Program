import tkinter as tk
from tkinter import messagebox
import math


# A class that holds a window and some functions to manipulate it.
class Window:
	# A constructor for creating a window
	def __init__(self, name):
		self.border = tk.Tk()
		self.border.title(name)
		self.border.iconphoto(False, tk.PhotoImage(file="icon.png"))
		self.frame = tk.Frame(self.border)
		self.frame.pack()


# An exception that will be raised by the valid_float function if it receives an exception to tell
# the conversion functions not to convert the non existent return value
class DoNotContinue(Exception):
	pass


# Some exceptions for various unexpected values
class IsBlank(Exception):
	pass


class IsInfinite(Exception):
	pass


class IsNaN(Exception):
	pass


class IsBelowAbsoluteZero(Exception):
	pass


# A function that converts a value to a float and makes sure that it is a valid float
def valid_float(var_in):
	try:
		if var_in == "":
			raise IsBlank
		out = float(var_in)
		if out == math.inf or out == -math.inf:
			raise IsInfinite
		if math.isnan(out):
			raise IsNaN
		return out
	except ValueError:
		messagebox.showerror("Error", 'The number you entered is not a valid real number. Please enter a valid real number eg. "3.7".')
	except IsBlank:
		messagebox.showerror("Error", 'You have not entered anything into the entry box. Please click on the box above the "To °C" and "To °F" buttons and enter a number.')
	except IsInfinite:
		messagebox.showerror("Error", 'The number you entered is infinite, please enter a finite number eg. "4.5".')
	except IsNaN:
		messagebox.showerror("Error", 'The number you entered is not a number, please enter a number eg. "4.5".')
	except Exception as exception:
		messagebox.showerror("Error", 'Other or unknown error: "{}", "{}"'.format(type(exception).__name__, exception))
	raise DoNotContinue


def main():
	# Convert °F to °C
	def to_c():
		try:
			num = valid_float(text_box_val.get())
			if num < -273.15:
				raise IsBelowAbsoluteZero
			text_box_val.set(valid_float((num - 30) / 2))
		except DoNotContinue:
			pass
		except IsBelowAbsoluteZero:
			messagebox.showerror("Error", 'Value is below absolute zero. Please enter a number above absolute zero eg. "3".')

	# Convert °C to °F
	def to_f():
		try:
			num = valid_float(text_box_val.get())
			if num < -459.67:
				raise IsBelowAbsoluteZero
			text_box_val.set(valid_float(num * 2 + 30))
		except DoNotContinue:
			pass
		except IsBelowAbsoluteZero:
			messagebox.showerror("Error", 'Value is below absolute zero. Please enter a number above absolute zero eg. "3".')

	def help_window():
		messagebox.showinfo("Help", """Enter a number into the text box above “To °C” and “To °F” then use:\n“To °C” to convert a fahrenheit temperature to a celsius temperature.\n“To °F” to convert a celsius temperature to a fahrenheit temperature.""")

	main_window = Window("Unit Converter")  # Create Main Window

	text_box_val = tk.StringVar()  # Holds text box value

	text_box = tk.Entry(main_window.frame, width=50, textvariable=text_box_val)  # Text box
	text_box.grid(row=0, column=0, columnspan=2)
	to_c_button = tk.Button(main_window.frame, text="To °C", width=20, command=to_c)  # To °C button
	to_c_button.grid(row=1, column=0)
	to_f_button = tk.Button(main_window.frame, text="To °F", width=20, command=to_f)  # To °F button
	to_f_button.grid(row=1, column=1)
	help_button = tk.Button(main_window.frame, text="Help", width=20, command=help_window)  # To °F button
	help_button.grid(row=2, column=0)

	main_window.border.mainloop()  # Enter a loop to keep the window open until the the X button is pressed.


# Entrypoint
if __name__ == "__main__":
	main()
