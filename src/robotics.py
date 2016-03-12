import math
import random

# Initialize Parameters
x = 0.0
y = 0.0
theta = 0.0
speed = 0.0

maximum_speed = 0.1
sensor_cone_width = math.pi/2.9
sensor_angles = [math.pi/3, 0, -math.pi/3]
time_scale = 1 / 10.0
number_of_obstacles = 10

def do_simulation_step(environment):
	'''Given an environment, give the robot's next position and orientation'''
	global x
	global y
	global theta
	global speed

	sensor_data = [ get_sensor_data(environment, x, y, theta, sensor_angle) for sensor_angle in sensor_angles ]
	forcelets = [ forcelet(sd, sa) for sd, sa in zip(sensor_data, sensor_angles) ]

	x_dot = math.cos(theta) * maximum_speed * sigma(speed)
	y_dot = math.sin(theta) * maximum_speed * sigma(speed)
	speed_dot = -speed - 4.0 + (8.0/5.0) * min(min(sensor_data), 5.0)
	theta_dot = sum(forcelets) + random.gauss(0, (0.4 - abs(speed) / 10))

	x = x + x_dot * time_scale
	y = y + y_dot * time_scale
	theta = theta + theta_dot * time_scale
	speed = speed + speed_dot * time_scale

	return x, y, theta

def get_sensor_data(environment, x, y, theta, sensor_angle, get_obstacle_coords=False):
	angle = theta + sensor_angle

	closest_distance = 2**30
	closest_obstacle = None
	for obs_y, row in enumerate(environment):
		for obs_x, obstacle in enumerate(row):
			if obstacle:
				obstacle_angle = math.atan2(obs_y - y, obs_x - x)
				angle_difference = math.atan2(math.sin(angle - obstacle_angle), math.cos(angle-obstacle_angle))
				if abs(angle_difference) < sensor_cone_width / 2:
					distance = math.sqrt((obs_x - x)**2 + (obs_y - y)**2)
					if distance < closest_distance:
						closest_distance = distance
						closest_obstacle = (obs_x, obs_y)

	if get_obstacle_coords == True:
		return closest_distance, closest_obstacle
	else:
		return closest_distance

def forcelet(sensor_reading, sensor_angle):
	lambd = 3.0 * math.exp(-sensor_reading / 1.0)
	sigma = math.atan(math.tan(sensor_cone_width/2.0) + (1.0 / (1.0 + sensor_reading)))
	force = lambd * (-sensor_angle) * math.exp(- (sensor_angle)**2/(2*sigma**2))
	return force

def sigma(x, beta=1.0):
	return 1.0 / (1.0 + math.exp(- beta * x))

def initialize_environment(height, width):
	'''Takes width and height and creates a 2D environment of that size'''
	environment = [ [True] + [False]*(width-2) + [True] for _ in range(height) ]
	environment[0] = [True]*width
	environment[-1] = [True]*width

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

		if not environment[y][x]:
			break

	theta = random.uniform(0, 2 * math.pi)
	speed = 0