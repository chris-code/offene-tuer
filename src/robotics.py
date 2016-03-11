import math
import numpy

x = 10.0
y = 15.0
theta = math.pi/4

speed = 0.5
sensor_cone_width = math.pi/4
sensor_angles = [math.pi/3, math.pi/6, 0, -math.pi/6, -math.pi/3]
#~ sensor_angles = [math.pi/6, -math.pi/6]

number_of_obstacles = 10

def do_simulation_step(environment):
	'''Given an environment, give the robot's next position and orientation'''
	global x
	global y
	global theta

	sensor_readings = [get_sensor_readings(environment, x, y, theta, sensor_angle) for sensor_angle in sensor_angles]
	forcelets = [forcelet(sr, sa) for sr, sa in zip(sensor_readings, sensor_angles)]

	x_dot = (math.cos(theta) * speed)
	y_dot = (math.sin(theta) * speed)
	theta_dot = sum(forcelets) + numpy.random.normal(0, 0.1)

	#~ print( forcelets )
	#~ print( sum(forcelets) )
	#~ print( '{0:.3} {1:.3}'.format(x,y) )
	#~ print( int(round((theta / (2*math.pi) * 360 + 360) % 360)) )

	x = x + x_dot / 10
	y = y + y_dot / 10
	theta = theta + theta_dot / 10

	return x, y, theta

def get_sensor_readings(environment, x, y, theta, sensor_angle, get_obstacle_coords=False):
	angle = theta + sensor_angle

	closest_distance = 2**30
	closest_obstacle = None
	for obs_y, row in enumerate(environment):
		for obs_x, obstacle in enumerate(row):
			if obstacle == True:
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

def initialize_environment(height, width):
	'''Takes width and height and creates a 2D environment of that size'''
	environment = numpy.zeros(shape=(height, width), dtype=numpy.bool_)
	environment[:,0] = True
	environment[:,-1] = True
	environment[0,:] = True
	environment[-1,:] = True

	add_obstacles(environment, number_of_obstacles)

	return environment

def add_obstacles(environment, number_of_obstacles):
	environment_height, environment_width = environment.shape

	for o in range(number_of_obstacles):
		x_center = numpy.random.uniform(2, environment_width-3)
		y_center = numpy.random.uniform(2, environment_height-3)

		x_center = int(round(x_center))
		y_center = int(round(y_center))

		for x in range(x_center-1, x_center+2):
			for y in range(y_center-1, y_center+2):
				environment[y,x] = True

def print_status(environment, x, y, theta):
	status = environment.astype(numpy.uint8)
	status[status==0] = ord(' ')
	status[status==1] = ord('#')
	coordinates = (int(round(y)), int(round(x)))
	status[coordinates] = ord('R')

	sensor_readings = [get_sensor_readings(environment, x, y, theta, sensor_angle, get_obstacle_coords=True) for sensor_angle in sensor_angles]
	for distance, coords in sensor_readings:
		x, y = coords
		status[y,x] = ord('O')

	status = status[::-1,:]
	for row in status:
		ascii_symbols = [chr(value) for value in row]
		print(''.join(ascii_symbols))
	print('')

import time
if __name__ == '__main__':
	environment = initialize_environment(20, 60)

	while True:
		x, y, theta = do_simulation_step(environment)
		print_status(environment, x, y, theta)
		time.sleep(0.025)