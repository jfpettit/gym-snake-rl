from core_snake import Arena, Snake
from single_snake import SingleSnake
from multi_snake import MultiSnake
from render import Renderer, RGBifier
import numpy as np

if __name__ == '__main__':
	env = MultiSnake(num_foods=2, add_walls=True)
	env.reset()

	action = np.random.choice(len(env.arena.DIRS), size=2)
	for i in range(10):
	    output = env.step(action)
	    action = np.random.choice(len(env.arena.DIRS), size=2)
	    env.render()
	env.close()