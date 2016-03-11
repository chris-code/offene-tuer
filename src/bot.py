from tkinter import *
import math

arrow_length = 13
bot_radius = 15
bot_color = "#115EA6"

class Bot:
	def __init__(self, field, x, y, theta):
		self.field = field
		self.canvas = self.field.getCanvas()
		self.x = self._calcX(x)
		self.y = self.field.getDimensions()[1] - y - 1
		self.theta = theta
		self.circle_id = self.canvas.create_oval(self.x - bot_radius, self.y - bot_radius, self.x + bot_radius, self.y + bot_radius, fill=bot_color)
		head_x = math.cos(self.theta) * arrow_length
		head_y = math.sin(self.theta) * arrow_length
		self.line_id = self.canvas.create_line(self.x, self.y, self.x + head_x, self.y - head_y, fill="#000000", width=3)

	def moveToAndRotate(self, x, y, theta):
		self.x = self._calcX(x)
		self.y = self._calcY(y)
		self.theta = theta
		self.field.paint()

	def paint(self):
		self.canvas.coords(self.circle_id, self.x - bot_radius, self.y - bot_radius, self.x + bot_radius, self.y + bot_radius)
		head_x = math.cos(self.theta) * arrow_length
		head_y = math.sin(self.theta) * arrow_length
		self.canvas.coords(self.line_id, self.x, self.y, self.x + head_x, self.y - head_y)

	def _calcY(self, y):
		return self.field.getDimensions()[1] - (y + 0.5) * self.field.getScalingFactor()

	def _calcX(self, x):
		return (x + 0.5) * self.field.getScalingFactor()


