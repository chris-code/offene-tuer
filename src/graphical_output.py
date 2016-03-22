import math
import sys
if sys.version_info.major >= 3:
	from tkinter import *
else:
	from Tkinter import *
import obstacle
import bot

canvas_width = 900

class Field():
	def __init__(self, env):
		self.env = env
		self.scaling_factor = canvas_width / env.width
		self.width = canvas_width
		self.height = int(round(env.height * self.scaling_factor))

		self.bot = None
		self.obstacles = set()
		self.halt = False

		self.master = Tk()
		self.master.bind('<Escape>', self.close)
		self.canvas = Canvas(self.master, width=self.width, height=self.height, background="#000000", highlightthickness=0)
		self.canvas.bind('<ButtonRelease-3>', self.place_obstacle_callback)
		self.canvas.pack()

		for x_obs, y_obs in env:
			self.add_obstacle(x_obs, y_obs)

	def transformCoordinates(self, x, y):
		newX = (x + 0.5) * self.scaling_factor
		newY = self.height - (y + 0.5) * self.scaling_factor

		return newX, newY

	def transformLength(self, l):
		return l * self.scaling_factor

	def add_obstacle(self, x, y):
		obs = obstacle.Obstacle(self, x, y)
		self.obstacles.add(obs)

	def remove_obstacle(self, x, y):
		o = None
		for obs in self.obstacles:
			if obs.represented_coordinates == (x, y):
				o = obs
				break
		o.delete()
		self.obstacles.remove(o)

	def moveBot(self, x, y, theta):
		if not self.bot:
			self.bot = bot.Bot(self, x, y, theta)
		else:
			self.bot.moveToAndRotate(x, y, theta)

	def place_obstacle_callback(self, event):
		x = int(math.floor(event.x / self.scaling_factor))
		y = int(math.floor((self.height - event.y) / self.scaling_factor))

		if (x, y) not in self.env:
			self.env.add_obstacle(x, y)
			self.add_obstacle(x, y)
		else:
			self.env.remove_obstacle(x, y)
			self.remove_obstacle(x, y)

	def paint(self):
		self.bot.paint()
		self.master.update()

	def close(self, event):
		self.master.withdraw()
		self.halt = True
