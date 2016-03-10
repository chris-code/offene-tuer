from tkinter import *
import math

arrow_length = 22;
bot_radius = 25;
bot_color = "#115EA6"

class Bot:
	def __init__(self, field, x, y, theta):
		self.field = field
		self.canvas = self.field.getCanvas()
		self.x = x
		self.y = self.field.getDimensions()[1] - y - 1
		self.theta = theta
		print((self.x, self.y))

	def moveTo(self, x, y):
		self.x = x
		self.y = self.field.getDimensions()[1] - y - 1
		self.field.paint()

	def rotate(self, theta):
		self.theta = theta
		self.field.paint()

	def paint(self):
		self.canvas.create_oval(self.x - bot_radius, self.y - bot_radius, self.x + bot_radius, self.y + bot_radius, fill=bot_color)
		head_x = math.cos(self.theta) * arrow_length
		head_y = math.sin(self.theta) * arrow_length
		self.canvas.create_line(self.x, self.y, self.x + head_x, self.y - head_y, fill="#000000", width=3)

