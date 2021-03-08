import tkinter as tk


# A class that holds a window and some functions to manipulate it.
class Window:
	# A constructor for creating a window
	def __init__(self, name):
		self.border = tk.Tk()
		self.border.title(name)
		self.frame = tk.Frame(self.border)
		self.frame.pack()

		self.elements = []


def main():
	# Convert °F to °C
	def to_c():
		num = float(text_box_val.get())
		text_box_val.set((num - 30) / 2)

	# Convert °C to °F
	def to_f():
		num = float(text_box_val.get())
		text_box_val.set(num * 2 + 30)

	main_window = Window("Hi")  # Create Main Window

	text_box_val = tk.StringVar()  # Holds text box value

	text_box = tk.Entry(main_window.frame, width=50, textvariable=text_box_val)  # Text box
	text_box.grid(row=0, column=0, columnspan=2)
	to_c_button = tk.Button(main_window.frame, text="To °C", width=20, command=to_c)  # To °C button
	to_c_button.grid(row=1, column=0)
	to_f_button = tk.Button(main_window.frame, text="To °F", width=20, command=to_f)  # To °F button
	to_f_button.grid(row=1, column=1)

	main_window.border.mainloop()  # Enter a loop to keep the window open until the the X button is pressed.


# Entrypoint
if __name__ == "__main__":
	main()
