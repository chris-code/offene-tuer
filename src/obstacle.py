from tkinter import *

obstacle_color = "#F6FC7C"

class Obstacle:
	def __init__(self, field, x, y, width, height):
		self.field = field
		self.canvas = self.field.getCanvas()
		self.x = self._calcX(x)
		self.y = self._calcY(y)
		self.half_width = width / 2 * self.field.getScaleFactors()[0]
		self.half_height = height / 2 * self.field.getScaleFactors()[1]

	def paint(self):
		self.canvas.create_rectangle(self.x - self.half_width, self.y - self.half_height/2, self.x + self.half_width, self.y + self.half_height, fill=obstacle_color)

	def _calcY(self, y):
		return self.field.getDimensions()[1] - (y * self.field.getScaleFactors()[1])

	def _calcX(self, x):
		return x * self.field.getScaleFactors()[0]
