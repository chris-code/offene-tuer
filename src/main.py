import math
import time

from bot import Bot
from field import Field
from obstacle import Obstacle
import robotics

# canvas and environment height
environment_width = 30
environment_height = 20

canvas_width = 900
scaling_factor = canvas_width / environment_width
canvas_height = int(round(environment_height * scaling_factor))

# initialize
environment = robotics.initialize_environment(environment_height, environment_width)
field = Field(canvas_width, canvas_height, scaling_factor)
x, y, theta = robotics.do_simulation_step(environment)

# add obstacles
for y in range(environment_height):
	for x in range(environment_width):
		if environment[y][x]:
			field.addObstacle(Obstacle(field, x, y))

# add bot
r2d2 = Bot(field, x, y, theta)
field.setBot(r2d2)

while(not field.halt):
	x, y, theta = robotics.do_simulation_step(environment)
	r2d2.moveToAndRotate(x, y, theta)
