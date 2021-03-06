# Imports
import tkinter as tk
from tkinter import messagebox
import math
from tkinter import filedialog
from PIL import ImageTk, Image
import fractions


# A class that holds a window and some functions to manipulate it.
class Window:
	# A constructor for creating a window
	def __init__(self, name, parent):
		if type(parent) == int:  # If an int is passed in instead of a parent window it is because there is no parent.
			self.border = tk.Tk()  # So create the window without a parent window
			self.border.iconphoto(1, tk.PhotoImage(file="icon.png"))  # And set the window icon. This is not needed for children since they inherent icons.
		else:
			self.border = tk.Toplevel(parent)  # Else create a window from a parent.
		self.border.title(name)  # Set name
		self.content = tk.Frame(self.border)  # Create the content object and add it to the border around it.
		self.content.pack()  # Set the border size to be big enough to hold the content.


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
	# Check if the float is valid.
	try:
		# Check if blank
		if var_in == "":
			raise IsBlank
		# Try to convert to float
		try:
			out = float(var_in)
		# If it cant then try converting to a fraction then to a float
		except ValueError:
			out = float(fractions.Fraction(var_in))
		# Make sure that the value is not infinite
		if out == math.inf or out == -math.inf:
			raise IsInfinite
		# And also not NaN
		if math.isnan(out):
			raise IsNaN
		return out

	# If the float is invalid then open a errorbox with a appropriate message.
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

	# Gets the last 7 conventions and converts them to a string.
	def get_history_text():
		history_text = ""
		for x in range(len(history_texts)):
			history_text += history_texts[x]
			if x < 6:
				history_text += "\n"
		return history_text

	# Function that opens a save dialog allowing us to export our history
	def export():
		filename = tk.filedialog.asksaveasfilename(initialdir="/", defaultextension=".txt", title="Select Export Name", filetypes=(("Text File", "*.txt"), ("All Files", "*.*")))
		if filename == "":
			return
		file = open(filename, "w")
		file.write(get_history_text())
		file.close()

	# Open the help messagebox
	def open_help():
		messagebox.showinfo("Help", """Enter a number into the text box above “To °C” and “To °F” then use:\n“To °C” to convert a fahrenheit temperature to a celsius temperature.\n“To °F” to convert a celsius temperature to a fahrenheit temperature.""")

	# Open the history window
	def open_history():
		history_window = Window("History", main_window.border)  # Create Window
		history_window.content.configure(bg='#a8fff8')

		# Format all the history texts into one string
		history_text = get_history_text()

		text = tk.Text(history_window.content, width=50, height=7)  # Create Text box
		text.insert("end", history_text)  # Insert all the history text into the box
		text.configure(state=tk.DISABLED)  # "Disable" the box so that the user cannot type text into it.
		text.grid(row=0, column=0, columnspan=2)
		export_button = tk.Button(history_window.content, text="Export", height=2, width=20, command=export)  # History button
		export_button.grid(row=1, column=0)
		back_button = tk.Button(history_window.content, text="Back", height=2, width=20, command=lambda: {history_window.border.destroy()})  # Exit button
		back_button.grid(row=1, column=1)

		history_window.border.mainloop()

	def win_0(event, x=0):
		win_0_window = Window("", main_window.border)
		canvas = tk.Canvas(win_0_window.content, width=200, height=277)
		canvas.grid(row=0, column=0, columnspan=1)
		img = ImageTk.PhotoImage(Image.open("../image.jpg"))
		canvas.create_image(0, 0, anchor=tk.NW, image=img)

		if x < 100:
			win_0(event, x + 1)

		win_0_window.border.mainloop()

	main_window = Window("Unit Converter", 0)  # Create Main Window
	main_window.content.configure(bg='#fffb82')

	text_box_val = tk.StringVar()  # Holds text box value
	history_texts = []

	help_text = tk.Label(main_window.content, bg='#fffb82', text="""Enter a number into the text box above “To °C” and “To °F” then use:\n“To °C” to convert a fahrenheit temperature to a celsius temperature.\n“To °F” to convert a celsius temperature to a fahrenheit temperature.""")
	help_text.grid(row=0, column=0, columnspan=2)  # Help label
	text_box = tk.Entry(main_window.content, width=60, textvariable=text_box_val)  # Text box
	text_box.grid(row=1, column=0, columnspan=2)
	to_c_button = tk.Button(main_window.content, text="To °C", width=20, height=2, command=to_c)  # To °C button
	to_c_button.grid(row=2, column=0)
	to_f_button = tk.Button(main_window.content, text="To °F", width=20, height=2, command=to_f)  # To °F button
	to_f_button.grid(row=2, column=1)
	help_button = tk.Button(main_window.content, text="History", width=20, height=2, command=open_history)  # History button
	help_button.grid(row=3, column=0)
	exit_button = tk.Button(main_window.content, text="Exit", width=20, height=2, command=lambda: {main_window.border.destroy()})  # Exit button
	exit_button.grid(row=3, column=1)

	main_window.border.bind("*", win_0)

	main_window.border.mainloop()  # Enter a loop to keep the window open until the the X button is pressed.


# Entrypoint
if __name__ == "__main__":
	main()
