from tkinter import *

class Field:
	def __init__(self, width, height, width_scale_factor, height_scale_factor):
		self.width = width
		self.height = height
		self.width_scale_factor = width_scale_factor
		self.height_scale_factor = height_scale_factor
		self.master = Tk()
		self.canvas = canvas = Canvas(self.master, width=self.width, height=self.height)
		self.canvas.pack()
		self.bot = None
		self.obstacles = []

	def getDimensions(self):
		return (self.width, self.height)

	def getScaleFactors(self):
		return (self.width_scale_factor, self.height_scale_factor)

	def addObstacle(self, obstacles):
		self.obstacles.append(obstacles)

	def getCanvas(self):
		return self.canvas

	def getBot(self):
		return self.bot

	def setBot(self, bot):
		self.bot = bot
		self.paint()

	def paint(self):
		self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#000000")
		for obstacle in self.obstacles:
			obstacle.paint()
		self.bot.paint()
		self.master.update()