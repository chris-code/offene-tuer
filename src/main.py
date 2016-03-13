import math
import time
#~ from terminal_output import Field
from graphical_output import Field
import robotics

# Initialize robotics
environment = robotics.initialize_environment()
x, y, theta = robotics.do_simulation_step(environment)

# Initialize GUI
field = Field(robotics.environment_width, robotics.environment_height)

# Add obstacles to GUI
for y, row in enumerate(environment):
	for x, element in enumerate(row):
		if element:
			field.addObstacle(x, y)

# Create bot
field.initializeBot(x, y, theta)

# Main loop, runs indefinitely
while(not field.halt):
	x, y, theta = robotics.do_simulation_step(environment)
	field.moveBot(x, y, theta)
	field.paint()
