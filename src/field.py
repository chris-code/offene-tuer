from tkinter import *
import obstacle
import bot

canvas_width = 900

class Field:
	def __init__(self, data_width, data_height):
		self.scaling_factor = canvas_width / data_width
		self.width = canvas_width
		self.height = int(round(data_height * self.scaling_factor))

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

	def addObstacle(self, x, y):
		obs = obstacle.Obstacle(self, x, y)
		self.obstacles.append(obs)

	def initializeBot(self, x, y, theta):
		self.bot = bot.Bot(self, x, y, theta)

	def moveBot(self, x, y, theta):
		self.bot.moveToAndRotate(x, y, theta)

	def paint(self):
		self.bot.paint()
		self.master.update()

	def close(self, event):
		self.master.withdraw()
		self.halt = True
