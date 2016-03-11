from tkinter import *

obstacle_color = "#F6FC7C"

class Obstacle:
	def __init__(self, field, x, y):
		self.field = field
		self.canvas = self.field.getCanvas()

		self.x = self._calcX(x)
		self.y = self._calcY(y)
		self.width = self.field.getScalingFactor()
		self.height = self.field.getScalingFactor()

		self.rect_id = self.canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y - self.height, fill=obstacle_color)

	def _calcY(self, y):
		return self.field.getDimensions()[1] - (y * self.field.getScalingFactor())

	def _calcX(self, x):
		return x * self.field.getScalingFactor()
