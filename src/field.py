from tkinter import *

class Field:
	def __init__(self, width, height, width_scale_factor, height_scale_factor):
		self.width = width
		self.height = height
		self.width_scale_factor = width_scale_factor
		self.height_scale_factor = height_scale_factor
		self.master = Tk()
		self.master.bind('<Escape>', self.close)
		#~ self.master.configure(background='black')
		self.canvas = Canvas(self.master, width=self.width, height=self.height, background="#000000", highlightthickness=0)
		self.canvas.pack()
		self.bot = None
		self.obstacles = []
		self.halt = False

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
		self.bot.paint()
		self.master.update()

	def close(self, event):
		self.master.withdraw()
		self.halt = True
