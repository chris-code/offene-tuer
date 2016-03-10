import numpy

x = 10.0
y = 10.0
theta = 0.0
speed = 3.0

def do_simulation_step(environment):
	'''For a given an environment, give the robot's next position and orientation'''

	return x, y, theta

def initialize_environment(height, width):
	'''Takes width and height and creates a 2D environment of that size'''
	environment = numpy.zeros(shape=(height, width), dtype=numpy.bool_)
	environment[:,0] = True
	environment[:,-1] = True
	environment[0,:] = True
	environment[-1,:] = True

	return environment