import math
import time

from bot import Bot
from field import Field
from obstacle import Obstacle
import robotics

# canvas and environment height
canvas_width = 900
canvas_height = 300

environment_width = 30
environment_height = 10

# calculate scale factors
width_scale_factor = canvas_width / environment_width
height_scale_factor = canvas_height / environment_height

# initialize
environment = robotics.initialize_environment(environment_height, environment_width)
field = Field(canvas_width, canvas_height, width_scale_factor, height_scale_factor)
x, y, theta = robotics.do_simulation_step(environment)
r2d2 = Bot(field, x, y, theta)

for y in range(10):
	for x in range(30):
		if environment[y][x]:
			field.addObstacle(Obstacle(field, x, y, 1, 1))


field.setBot(r2d2)

while(True):
	x, y, theta = robotics.do_simulation_step(environment)
	field.getBot().moveToAndRotate(x, y, theta)
	#time.sleep(0.1)
