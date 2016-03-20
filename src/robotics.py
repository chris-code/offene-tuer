import math
import random

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

# Sanitize input, convert to radians, set up sensors
number_of_sensors = int(round(number_of_sensors))
number_of_obstacles = int(round(number_of_obstacles))
sensor_cone_width *= (1.0 / 360.0) * 2 * math.pi
sensor_mount_angle *= (1.0 / 360.0) * 2 * math.pi
sensor_angles = [sensor_mount_angle * (-0.5 + i * 1.0 / (number_of_sensors-1)) for i in range(number_of_sensors)]
sensor_angles.reverse()

def do_simulation_step(environment):
	'''Given an environment, give the robot's next position and orientation'''

	global x, y, theta, speed

	sensor_data = [ get_sensor_data(environment, x, y, theta, sensor_angle) for sensor_angle in sensor_angles ]
	forcelets = [ forcelet(sd, sa) for sd, sa in zip(sensor_data, sensor_angles) ]

	x_dot = math.cos(theta) * maximum_speed * sigmoid(speed)
	y_dot = math.sin(theta) * maximum_speed * sigmoid(speed)
	speed_dot = -speed - 4.0 + (8.0/5.0) * min(min(sensor_data), 5.0)
	theta_dot = sum(forcelets) + random.gauss(0, 0.1 - abs(speed) / 40)

	obstacle_force_x, obstacle_force_y = prevent_block_crossing(environment, x, y)
	x_dot += obstacle_force_x
	y_dot += obstacle_force_y

	x = x + x_dot * time_scale
	y = y + y_dot * time_scale + obstacle_force_y
	theta = theta + theta_dot * time_scale
	speed = speed + speed_dot * time_scale

	return x, y, theta

def get_sensor_data(environment, x, y, theta, sensor_angle):
	real_sensor_angle = theta + sensor_angle

	closest_distance = 2**30
	for obs_y, row in enumerate(environment):
		for obs_x, obstacle in enumerate(row):
			if obstacle:
				obstacle_angle = math.atan2(obs_y - y, obs_x - x)
				angle_difference = math.atan2(math.sin(real_sensor_angle - obstacle_angle), math.cos(real_sensor_angle - obstacle_angle))
				if abs(angle_difference) < sensor_cone_width / 2.0:
					distance = math.sqrt((obs_x - x)**2 + (obs_y - y)**2)
					closest_distance = min(closest_distance, distance)
	return closest_distance

def forcelet(sensor_reading, sensor_angle):
	lambd = repulsion_force * math.exp(-sensor_reading / distance_decay)
	sigma = math.atan(math.tan(sensor_cone_width/2.0) + (1.0 / (1.0 + sensor_reading)))
	force = lambd * (-sensor_angle) * math.exp(- (sensor_angle)**2/(2*sigma**2))
	return force

def sigmoid(x, beta=1.0):
	return 1.0 / (1.0 + math.exp(- beta * x))

def distance(x1, y1, x2, y2):
	return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def prevent_block_crossing(environment, x, y):
	'''This function prevents the robot from entering a square occupied by an obstacle.
	It is a rudimentary way to implement the obstacles as an actual, physical barrier'''

	grid_x, grid_y = int(round(x)), int(round(y))
	move_x, move_y = 0, 0 # the movement change induced by obstacles

	# Check for collisions with all neighbors
	direct_neighbors = [(grid_x + offset_x, grid_y + offset_y) for offset_x, offset_y in [(1,0), (0,1), (-1,0), (0,-1)]]
	for n_x, n_y in direct_neighbors:
		if 0 <= n_x <= len(environment[0]) and 0 <= n_y <= len(environment):
			if environment[n_y][n_x] == True:
				if n_x == grid_x and abs(y - n_y) < 1: # upper / lower neighbor
					move_y += 1.0 / (y - n_y) # move away horizontally
				elif n_y == grid_y and abs(x - n_x) < 1: # left / right neighbor
					move_x += 1.0 / (x - n_x) # move away vertically

	return move_x / 100.0, move_y / 100.0

def initialize_environment():
	'''Takes width and height and creates a 2D environment of that size'''

	environment = [ [True] + [False]*(environment_width-2) + [True] for _ in range(environment_height) ]
	environment[0] = [True] * environment_width
	environment[-1] = [True] * environment_width

	add_obstacles(environment, number_of_obstacles)

	initialize_robot(environment)

	return environment

def add_obstacles(environment, number_of_obstacles):
	environment_height, environment_width = len(environment), len(environment[0])

	for _ in range(number_of_obstacles):
		x_center = random.uniform(2, environment_width-3)
		y_center = random.uniform(2, environment_height-3)

		x_center = int(round(x_center))
		y_center = int(round(y_center))

		for x in range(x_center-1, x_center+2):
			for y in range(y_center-1, y_center+2):
				environment[y][x] = True

def initialize_robot(environment):
	global x, y, theta, speed

	environment_height, environment_width = len(environment), len(environment[0])
	for _ in range(100):
		x = random.uniform(1, environment_width-2)
		y = random.uniform(1, environment_height-2)

		x = int(round(x))
		y = int(round(y))

		if environment[y][x] == False:
			break

	theta = random.uniform(0, 2 * math.pi)
	speed = 0
