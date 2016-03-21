import math
import random

class Robot:
	def __init__(self, x_start, y_start, maximum_speed, number_of_sensors, sensor_cone_width, sensor_mount_angle, repulsion_force, distance_decay, time_scale):
		self.x, self.y = x_start, y_start
		self.theta = random.uniform(0, math.pi*2)
		self.speed = 0

		self.maximum_speed = maximum_speed
		self.sensor_cone_width = sensor_cone_width * (1.0 / 360.0) * 2 * math.pi
		self.repulsion_force = repulsion_force
		self.distance_decay = distance_decay

		number_of_sensors = int(round(number_of_sensors))
		sensor_mount_angle *= (1.0 / 360.0) * 2 * math.pi
		self.sensor_angles = [sensor_mount_angle * (-0.5 + i * 1.0 / (number_of_sensors-1)) for i in range(number_of_sensors)]
		self.sensor_angles.reverse()

		self.time_scale = time_scale

	def step(self, env):
		'''Given an environment, give the robot's next position and orientation'''

		sensor_data = [ self.get_sensor_data(env, sa) for sa in self.sensor_angles ]
		forcelets = [ self.forcelet(sd, sa) for sd, sa in zip(sensor_data, self.sensor_angles) ]
		obstacle_force_x, obstacle_force_y = self.prevent_block_crossing(env)

		x_dot = math.cos(self.theta) * self.maximum_speed * sigmoid(self.speed)
		y_dot = math.sin(self.theta) * self.maximum_speed * sigmoid(self.speed)
		speed_dot = -self.speed - 4.0 + (8.0/5.0) * min(min(sensor_data), 5.0)
		theta_dot = sum(forcelets) + random.gauss(0, 0.1 - abs(self.speed) / 40)

		x_dot += obstacle_force_x
		y_dot += obstacle_force_y

		self.x += x_dot * self.time_scale
		self.y += y_dot * self.time_scale
		self.theta += theta_dot * self.time_scale
		self.speed += speed_dot * self.time_scale

		return self.x, self.y, self.theta, self.speed

	def get_sensor_data(self, env, sensor_angle):
		real_sensor_angle = self.theta + sensor_angle

		closest_distance = 2**30
		for obs_x, obs_y in env:
			obstacle_angle = math.atan2(obs_y - self.y, obs_x - self.x)
			angle_difference = math.atan2(math.sin(real_sensor_angle - obstacle_angle), math.cos(real_sensor_angle - obstacle_angle))
			if abs(angle_difference) < self.sensor_cone_width / 2.0:
				obs_distance = distance(obs_x, obs_y, self.x, self.y)
				closest_distance = min(closest_distance, obs_distance)
		return closest_distance

	def forcelet(self, sensor_reading, sensor_angle):
		lambd = self.repulsion_force * math.exp(-sensor_reading / self.distance_decay)
		sigma = math.atan(math.tan(self.sensor_cone_width/2.0) + (1.0 / (1.0 + sensor_reading)))
		force = lambd * (-sensor_angle) * math.exp(- (sensor_angle)**2/(2*sigma**2))
		return force

	def prevent_block_crossing(self, env):
		'''This function prevents the robot from entering a square occupied by an obstacle.
		It is a rudimentary way to implement the obstacles as an actual, physical barrier'''

		grid_x, grid_y = int(round(self.x)), int(round(self.y))
		move_x, move_y = 0, 0 # the movement change induced by obstacles

		# Check for collisions with all neighbors
		direct_neighbors = [(grid_x + offset_x, grid_y + offset_y) for offset_x, offset_y in [(1,0), (0,1), (-1,0), (0,-1)]]
		for n_x, n_y in direct_neighbors:
			if (n_x, n_y) in env:
				if n_x == grid_x and abs(self.y - n_y) < 1: # upper / lower neighbor
					move_y += 1.0 / (self.y - n_y) # move away horizontally
				elif n_y == grid_y and abs(self.x - n_x) < 1: # left / right neighbor
					move_x += 1.0 / (self.x - n_x) # move away vertically
		move_x, move_y = move_x / 100.0, move_y / 100.0

		return move_x, move_y



# Helper functions

def sigmoid(x, beta=1.0):
	return 1.0 / (1.0 + math.exp(- beta * x))

def distance(x1, y1, x2, y2):
	return math.sqrt((x1-x2)**2 + (y1-y2)**2)