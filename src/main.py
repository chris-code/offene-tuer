import math
import time

from bot import Bot
from field import Field
import robotics

canvas_width = 900
canvas_height = 600

field = Field(canvas_width, canvas_height)
r2d2 = Bot(field, 0, 0, math.pi)
field.setBot(r2d2)

environment = robotics.initialize_environment(10, 30)
for i in range(200):
	x, y, theta = robotics.do_simulation_step(environment)
	field.getBot().moveTo(x, y)
	field.getBot().rotate(theta)
	time.sleep(0.1)
