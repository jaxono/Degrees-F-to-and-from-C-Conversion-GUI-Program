import asyncio
import tkinter as tk
from tkinter import messagebox
import math

from PIL import ImageTk,Image


# A class that holds a window and some functions to manipulate it.
class Window:
	# A constructor for creating a window
	def __init__(self, name, parent=0):
		if type(parent) == int:
			self.border = tk.Tk()
			self.border.iconphoto(1, tk.PhotoImage(file="icon.png"))
		else:
			self.border = tk.Toplevel(parent)
		self.border.title(name)
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
			num_in = valid_float(text_box_val.get())
			if num_in < -273.15:
				raise IsBelowAbsoluteZero
			num_out = valid_float((num_in - 30) / 2)
			text_box_val.set(num_out)
			history_texts.append("{} °F to {} °C".format(num_in, num_out))
			if len(history_texts) > 7:
				history_texts.pop(0)
		except DoNotContinue:
			pass
		except IsBelowAbsoluteZero:
			messagebox.showerror("Error", 'Value is below absolute zero. Please enter a number above absolute zero eg. "3".')

	# Convert °C to °F
	def to_f():
		try:
			num_in = valid_float(text_box_val.get())
			if num_in < -459.67:
				raise IsBelowAbsoluteZero
			num_out = valid_float(num_in * 2 + 30)
			text_box_val.set(num_out)
			history_texts.append("{} °C to {} °F".format(num_in, num_out))
			if len(history_texts) > 7:
				history_texts.pop(0)
		except DoNotContinue:
			pass
		except IsBelowAbsoluteZero:
			messagebox.showerror("Error", 'Value is below absolute zero. Please enter a number above absolute zero eg. "3".')

	# Open the help messagebox
	def open_help():
		messagebox.showinfo("Help", """Enter a number into the text box above “To °C” and “To °F” then use:\n“To °C” to convert a fahrenheit temperature to a celsius temperature.\n“To °F” to convert a celsius temperature to a fahrenheit temperature.""")

	# Open the history window
	def open_history():
		history_window = Window("History", main_window.border)  # Create Window

		# Format all the history texts into one string
		history_text = ""
		for x in range(len(history_texts)):
			history_text += history_texts[x]
			if x < 6:
				history_text += "\n"

		text = tk.Text(history_window.frame, width=50, height=7)  # Create Text box
		text.insert("end", history_text)  # Insert all the history text into the box
		text.configure(state=tk.DISABLED)  # "Disable" the box so that the user cannot type text into it.
		text.grid(row=0, column=0, columnspan=1)

		history_window.border.mainloop()

	def win_0(event, x=0):
		#for x in range(100):
		win_0_window = Window("", main_window.border)
		canvas = tk.Canvas(win_0_window.frame, width=256, height=354)
		canvas.grid(row=0, column=0, columnspan=1)
		img = ImageTk.PhotoImage(Image.open("image.jpg"))
		canvas.create_image(0, 0, anchor=tk.NW, image=img)

		if x < 100:
			win_0(0, x + 1)

		win_0_window.border.mainloop()

	main_window = Window("Unit Converter")  # Create Main Window

	text_box_val = tk.StringVar()  # Holds text box value
	history_texts = []

	text_box = tk.Entry(main_window.frame, width=50, textvariable=text_box_val)  # Text box
	text_box.grid(row=0, column=0, columnspan=2)
	to_c_button = tk.Button(main_window.frame, text="To °C", width=20, command=to_c)  # To °C button
	to_c_button.grid(row=1, column=0)
	to_f_button = tk.Button(main_window.frame, text="To °F", width=20, command=to_f)  # To °F button
	to_f_button.grid(row=1, column=1)
	help_button = tk.Button(main_window.frame, text="Help", width=20, command=open_help)  # Help button
	help_button.grid(row=2, column=0)
	help_button = tk.Button(main_window.frame, text="History", width=20, command=open_history)  # History button
	help_button.grid(row=2, column=1)

	main_window.border.bind("*", win_0)

	#win2 = tk.Toplevel(main_window.border)

	main_window.border.mainloop()  # Enter a loop to keep the window open until the the X button is pressed.


# Entrypoint
if __name__ == "__main__":
	main()
