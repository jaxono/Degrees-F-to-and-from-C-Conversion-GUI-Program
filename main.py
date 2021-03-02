import tkinter as tk


class Window:
	def __init__(self, name):
		self.border = tk.Tk()
		self.border.title(name)
		self.frame = tk.Frame(self.border)
		self.frame.pack()

		self.elements = []

	def pack_all(self):
		for object in self.elements:
			object.pack()


def main():
	main_window = Window("Hi")

	main_window.elements.append(tk.Label(main_window.frame, text="Label"))

	main_window.pack_all()

	main_window.border.mainloop()


if __name__ == "__main__":
	main()
