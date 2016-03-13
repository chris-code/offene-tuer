import time

class Field:
	def __init__(self, data_width, data_height):
		self.bot = None
		self.array = [' ' * data_width for _ in range(data_height)]
		self.halt = False

	def addObstacle(self, x, y):
		self.array[y] = self.array[y][:x] + '#' + self.array[y][x+1:]

	def initializeBot(self, x, y, theta):
		self.bot_coordinates = (x, y, theta)

	def moveBot(self, x, y, theta):
		self.bot_coordinates = (x, y, theta)

	def paint(self):
		bot_x, bot_y, bot_theta = self.bot_coordinates
		bot_x, bot_y = int(round(bot_x)), int(round(bot_y))

		for row_number, row_data in enumerate(self.array):
			if row_number != bot_y:
				print(row_data)
			else:
				row_with_bot = row_data[:bot_x] + 'b' + row_data[bot_x+1:]
				print(row_with_bot)
		print('')

		time.sleep(0.01)