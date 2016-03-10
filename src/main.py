import math
import time

from bot import Bot
from field import Field

canvas_width = 900
canvas_height = 600

field = Field(canvas_width, canvas_height)
r2d2 = Bot(field, 0, 0, math.pi)
field.setBot(r2d2)

y = 0
x = 0
for i in range(200):
	x += 1
	y += 1
	time.sleep(0.1)
	field.getBot().moveTo(x, y)
