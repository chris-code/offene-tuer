import sys
if sys.version_info.major >= 3:
	from tkinter import *
else:
	from Tkinter import *
import math

arrow_length = 0.5
radius = 0.45
bot_color = "#115EA6"

class Bot():
	def __init__(self, field, x, y, theta):
		self.field = field
		self.canvas = self.field.canvas
		self.radius = self.field.transformLength(radius)
		self.arrow_length = self.field.transformLength(arrow_length)

		self.moveToAndRotate(x, y, theta)

		self.circle_id = self.canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius, fill=bot_color)
		head_x = math.cos(self.theta) * self.arrow_length
		head_y = math.sin(self.theta) * self.arrow_length
		self.line_id = self.canvas.create_line(self.x, self.y, self.x + head_x, self.y - head_y, fill="#000000", width=3)

	def moveToAndRotate(self, x, y, theta):
		self.x, self.y = self.field.transformCoordinates(x, y)
		self.theta = theta

	def paint(self):
		self.canvas.coords(self.circle_id, self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius)
		head_x = math.cos(self.theta) * self.arrow_length
		head_y = math.sin(self.theta) * self.arrow_length
		self.canvas.coords(self.line_id, self.x, self.y, self.x + head_x, self.y - head_y)