from gym.envs.registration import register

register(
	id='AloneSnake-v0',
	entry_point='gym_snakerl.envs:SingleSnake',
)

register(
	id='ManySnake-v0',
	entry_point='gym_snakerl.envs:MultiSnake',
)
