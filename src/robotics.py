"""This module controls [AI]-Bot's movements."""

import math
import random


class Robot():
	"""This Class implements the algorithms to controll and simulate [AI]-Bot."""

	def __init__(
			self, x_start, y_start, maximum_speed, number_of_sensors, sensor_cone_width,
			sensor_mount_angle, repulsion_force, distance_decay, time_scale):
		"""Save parameters and initialize the [AI]-Bot's internal state."""
		self.x, self.y = x_start, y_start
		self.theta = random.uniform(0, math.pi * 2)
		self.speed = 0

		self.maximum_speed = maximum_speed
		self.sensor_cone_width = sensor_cone_width * (1.0 / 360.0) * 2 * math.pi
		self.repulsion_force = repulsion_force
		self.distance_decay = distance_decay

		number_of_sensors = int(round(number_of_sensors))
		sensor_mount_angle *= (1.0 / 360.0) * 2 * math.pi
		self.sensor_angles = [
			sensor_mount_angle * (-0.5 + i * 1.0 / (number_of_sensors - 1))
			for i in range(number_of_sensors)
		]
		self.sensor_angles.reverse()

		self.stuckness_score = 0

		self.time_scale = time_scale

	def step(self, env):
		"""Given an environment, return the robot's next position and orientation."""
		sensor_data = self.get_sensor_data(env)
		narrowness_score = self.get_narrowness_score(sensor_data)

		# Physics prevents you from entering obstacles
		obstacle_force_x, obstacle_force_y = self.prevent_block_crossing(env)

		# Calculate movement change
		x_dot = math.cos(self.theta) * self.maximum_speed * sigmoid(self.speed, beta=4.0)
		y_dot = math.sin(self.theta) * self.maximum_speed * sigmoid(self.speed, beta=4.0)
		x_dot += obstacle_force_x
		y_dot += obstacle_force_y

		# Calculate orientation change
		forcelets = [self.forcelet(sd, sa) for sd, sa in zip(sensor_data, self.sensor_angles)]
		stuckness_coeff = sigmoid(self.stuckness_score - 0.78, beta=64)
		theta_dot = sum(forcelets) * (1 - stuckness_coeff)
		theta_dot += (math.pi / 3) * stuckness_coeff

		# Calculate speed change
		speed_dot = 3.0 * (-self.speed - 1.0 + 2.0 * (1 - narrowness_score))

		# Calculate change in stuckness score
		stuckness_score_dot = -self.stuckness_score + narrowness_score

		# Update move, rotate, change speed and stuckness score
		self.x += x_dot * self.time_scale
		self.y += y_dot * self.time_scale
		self.theta += theta_dot * self.time_scale
		self.speed += speed_dot * self.time_scale
		self.stuckness_score += stuckness_score_dot * self.time_scale

		return self.x, self.y, self.theta, self.speed

	def get_sensor_data(self, env):
		"""Return the readings from the robot's sensors."""
		sensor_data = []
		distances = env.get_distances(self.x, self.y)  # Distance to every obstacle
		angles = env.get_angles(self.x, self.y)  # Angle to every obstacle

		for sensor_angle in self.sensor_angles:
			absolute_sa = self.theta + sensor_angle

			closest_distance = 2**30
			for obs_x, obs_y in env:
				angle_difference = math.atan2(
					math.sin(absolute_sa - angles[(obs_x, obs_y)]),
					math.cos(absolute_sa - angles[(obs_x, obs_y)])
				)
				if abs(angle_difference) < self.sensor_cone_width / 2.0:
					closest_distance = min(closest_distance, distances[(obs_x, obs_y)])
			sensor_data.append(closest_distance)

		return sensor_data

	def forcelet(self, sensor_reading, sensor_angle):
		"""Compute force induced by sensor reading."""
		lambd = self.repulsion_force * math.exp(-sensor_reading / self.distance_decay)
		sigma = math.atan(
			math.tan(self.sensor_cone_width / 2.0)
			+
			(1.0 / (1.0 + sensor_reading))
		)
		force = lambd * (-sensor_angle) * math.exp(- (sensor_angle)**2 / (2*sigma**2))
		return force

	def get_narrowness_score(self, sensor_data):
		"""Return a value indicating how cramped the robot feels."""
		weighted_distances = [6.0]
		for sensor_value, sensor_angle in zip(sensor_data, self.sensor_angles):
			sigma = 1.25
			weighted_distance = min(sensor_value, 6.0) / math.exp(- sensor_angle**2 / (2 * sigma**2))
			weighted_distances.append(weighted_distance)

		return 1 - min(weighted_distances) / 6.0

	def prevent_block_crossing(self, env):
		"""
		Prevent the robot from entering a square occupied by an obstacle.

		It is a rudimentary way to implement the obstacles as an actual, physical barrier.
		"""
		grid_x, grid_y = int(round(self.x)), int(round(self.y))
		move_x, move_y = 0, 0  # the movement change induced by obstacles

		# Check for collisions with all neighbors
		direct_neighbors = [(grid_x + offset_x, grid_y + offset_y)
			for offset_x, offset_y in [(1, 0), (0, 1), (-1, 0), (0, -1)]]
		for n_x, n_y in direct_neighbors:
			if (n_x, n_y) in env:
				if n_x == grid_x and abs(self.y - n_y) < 0.9:  # upper / lower neighbor
					move_y += 1.0 / (self.y - n_y)  # move away horizontally
				elif n_y == grid_y and abs(self.x - n_x) < 0.9:  # left / right neighbor
					move_x += 1.0 / (self.x - n_x)  # move away vertically

		move_x, move_y = self.maximum_speed * move_x, self.maximum_speed * move_y
		return move_x, move_y


# Helper functions

def sigmoid(value, beta=1.0):
	"""Compute the value of the sigmoid function with slope beta at position value."""
	return 1.0 / (1.0 + math.exp(- beta * value))


def distance(x_1, y_1, x_2, y_2):
	"""Compute the distance of two points."""
	return math.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)
