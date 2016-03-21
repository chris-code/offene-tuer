import robotics
import environment
from terminal_output import Field

# Robot parameters
maximum_speed = 0.1 # Less than 0.3 is reasonable
number_of_sensors = 3 # Must be at least two
sensor_cone_width = 47
sensor_mount_angle = 90
repulsion_force = 3.0
distance_decay = 1.5

# Environment and simulation parameters
environment_width = 30
environment_height = 20
number_of_obstacles = 10
time_scale = 1 / 10.0

# Initialize environment
env = environment.Environment(environment_width, environment_height)
env.add_random_obstacles(number_of_obstacles)

# Initialize robot
x_start, y_start = env.get_free_position()
rob = robotics.Robot(x_start, y_start, maximum_speed, number_of_sensors, sensor_cone_width, sensor_mount_angle, repulsion_force, distance_decay, time_scale)
x, y, theta, speed = rob.step(env)

# Initialize GUI
field = Field(environment_width, environment_height)
for x_obs, y_obs in env:
	field.addObstacle(x_obs, y_obs)
field.initializeBot(x_start, y_start, theta)

# Main loop, runs indefinitely
while(not field.halt):
	x, y, theta, speed = rob.step(env)
	field.moveBot(x, y, theta)
	field.paint()
