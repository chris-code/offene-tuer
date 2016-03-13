import sys
if sys.version_info.major >= 3:
	from tkinter import *
else:
	from Tkinter import *

obstacle_color = "#F6FC7C"

obstacle_width = 1.0
obstacle_height = 1.0

class Obstacle:
	def __init__(self, field, x, y):
		self.field = field
		self.canvas = self.field.canvas

		self.x, self.y = self.field.transformCoordinates(x, y)
		self.half_width = self.field.transformLength(obstacle_width) / 2.0
		self.half_height = self.field.transformLength(obstacle_height) / 2.0

		top_left_x, top_left_y = self.x - self.half_width, self.y - self.half_height
		bottom_right_x, bottom_right_y = self.x + self.half_width, self.y + self.half_height
		self.rect_id = self.canvas.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill=obstacle_color)