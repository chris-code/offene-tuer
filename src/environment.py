import math
import random

class Environment:
	def __init__(self, width, height):
		'''Takes width and height and creates a 2D environment of that size'''

		self.width, self.height = width, height

		self.obstacles = { (x, 0) for x in range(self.width) }
		self.obstacles.update( [(x, self.height-1) for x in range(self.width)] )
		self.obstacles.update( [(0, y) for y in range(1, self.height-1)] )
		self.obstacles.update( [(self.width-1, y) for y in range(1, self.height-1)] )

	def get_distances(self, x, y):
		distances = {}
		for x_obs, y_obs in self.obstacles:
			distances[(x_obs, y_obs)] = math.sqrt((x_obs-x)**2 + (y_obs-y)**2)
		return distances

	def get_angles(self, x, y):
		angles = {}
		for x_obs, y_obs in self.obstacles:
			angles[(x_obs, y_obs)] = math.atan2(y_obs - y, x_obs - x)
		return angles

	def add_obstacle(self, x, y):
		self.obstacles.add((x, y))

	def add_random_obstacles(self, number_of_obstacles):
		number_of_obstacles = int(round(number_of_obstacles))

		for _ in range(number_of_obstacles):
			x_center = random.randint(1, self.width-2)
			y_center = random.randint(1, self.height-2)

			for x in range(x_center-1, x_center+2):
				for y in range(y_center-1, y_center+2):
					self.obstacles.add((x, y))

	def get_free_position(self):
		for _ in range(100):
			x = random.randint(0, self.width-1)
			y = random.randint(0, self.height-1)

			if not (x, y) in self.obstacles:
				return x, y

	def __iter__(self):
		return iter(self.obstacles)

	def __contains__(self, value):
		return value in self.obstacles