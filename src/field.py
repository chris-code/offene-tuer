from tkinter import *

class Field:
	def __init__(self, width, height, scaling_factor):
		self.width = width
		self.height = height
		self.scaling_factor = scaling_factor

		self.bot = None
		self.obstacles = []
		self.halt = False

		self.master = Tk()
		self.master.bind('<Escape>', self.close)
		self.canvas = Canvas(self.master, width=self.width, height=self.height, background="#000000", highlightthickness=0)
		self.canvas.pack()

	def transformCoordinates(self, x, y):
		newX = (x + 0.5) * self.scaling_factor
		newY = self.height - (y + 0.5) * self.scaling_factor

		return newX, newY

	def transformLength(self, l):
		return l * self.scaling_factor

	def addObstacle(self, obstacles):
		self.obstacles.append(obstacles)

	def paint(self):
		self.bot.paint()
		self.master.update()

	def close(self, event):
		self.master.withdraw()
		self.halt = True
