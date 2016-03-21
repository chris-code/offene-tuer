import time
import timeit

import robotics
import environment
from terminal_output import Field

# Robot parameters
maximum_speed = 6.0 # Squares per second
number_of_sensors = 5 # At least 2
sensor_cone_width = 42
sensor_mount_angle = 160
repulsion_force = 35.0
distance_decay = 1.5

# Environment and simulation parameters
environment_width = 30
environment_height = 20
number_of_obstacles = 10
time_scale = 1 / 120.0

# Initialize environment
env = environment.Environment(environment_width, environment_height)
env.add_random_obstacles(number_of_obstacles)

# Initialize robot
x_start, y_start = env.get_free_position()
rob = robotics.Robot(x_start, y_start, maximum_speed, number_of_sensors, sensor_cone_width, sensor_mount_angle, repulsion_force, distance_decay, time_scale)

# Initialize GUI
field = Field(environment_width, environment_height)
for x_obs, y_obs in env:
	field.addObstacle(x_obs, y_obs)

# Draw only one out of draw_counter_mod steps
# This is useful because we compute 1/time_scale simulation steps per second,
# which is usually a lot more than we want to draw
fps = 50.0 # 25 is NOT fluent motion
draw_counter = 0
draw_counter_mod = max( int(round( (1.0 / time_scale) / fps )), 1)

# Main loop, runs indefinitely
while(not field.halt):
	t_start = timeit.default_timer()
	x, y, theta, speed = rob.step(env)
	if draw_counter == 0:
		field.moveBot(x, y, theta)
		field.paint()
	draw_counter = (draw_counter + 1) % draw_counter_mod
	t_end = timeit.default_timer()

	if time_scale - (t_end - t_start) > 0.0011: # In this case the overhead of time.sleep is not an issue
		time.sleep( time_scale - (t_end - t_start) )
