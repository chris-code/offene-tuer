"""This module runs the main loop for the robotics simulation."""

import time
import timeit

import robotics
import environment
from graphical_output import Field

# [AI]-Bot parameters
MAXIMUM_SPEED = 6.0  # Squares per second
NUMBER_OF_SENSORS = 5  # At least 2
SENSOR_CONE_WIDTH = 42
SENSOR_MOUNT_ANGLE = 160
REPULSION_FORCE = 35.0
DISTANCE_DECAY = 1.5

# Environment and simulation parameters
ENVIRONMENT_WIDTH = 30
ENVIRONMENT_HEIGHT = 20
NUMBER_OF_OBSTACLES = 20
TIME_SCALE = 1 / 120.0


def main():
	"""Execute main function."""
	# Initialize environment
	env = environment.Environment(ENVIRONMENT_WIDTH, ENVIRONMENT_HEIGHT)
	env.add_random_obstacles(NUMBER_OF_OBSTACLES)

	# Initialize [AI]-Bot
	x_start, y_start = env.get_free_position()
	rob = robotics.Robot(
		x_start, y_start, MAXIMUM_SPEED, NUMBER_OF_SENSORS, SENSOR_CONE_WIDTH, SENSOR_MOUNT_ANGLE,
		REPULSION_FORCE, DISTANCE_DECAY, TIME_SCALE
	)

	# Initialize GUI
	field = Field(env)

	# Draw only one out of draw_counter_mod steps
	# This is useful because we compute 1/TIME_SCALE simulation steps per second,
	# which is usually a lot more than we want to draw
	fps = 50.0  # 25 is NOT fluent motion
	draw_counter = 0
	draw_counter_mod = max(int(round((1.0 / TIME_SCALE) / fps)), 1)

	# Main loop, runs indefinitely
	while not field.halt:
		t_start = timeit.default_timer()
		x_pos, y_pos, theta, _ = rob.step(env)
		if draw_counter == 0:
			field.moveBot(x_pos, y_pos, theta)
			field.paint()
		draw_counter = (draw_counter + 1) % draw_counter_mod
		t_end = timeit.default_timer()

		# In this case the overhead of time.sleep is not an issue
		if TIME_SCALE - (t_end - t_start) > 0.0011:
			time.sleep(TIME_SCALE - (t_end - t_start))


if __name__ == "__main__":
	main()
