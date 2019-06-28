from core_snake import Arena, Snake
from render import Renderer, RGBifier

import gym
from gym import spaces, utils, error
from gym.utils import seeding
import random
import numpy as np

class MultiSnake(gym.Env):
	metadata = {
        'render.modes': ['human','rgb_array'],
        'observation.types': ['raw', 'rgb', 'layered', 'vector']
}

	def __init__(self, size=(15, 15), num_snakes=2, step_limit=1000, dynamic_step_limit=1000, obs_type='vector', obs_zoom=1, num_foods=1,
	 die_on_eat=False, render_zoom=20, add_walls=False):
		self.SIZE=size
		self.num_snakes = num_snakes
		self.STEP_LIMIT = step_limit
		self.DYNAMIC_STEP_LIMIT = dynamic_step_limit

		self.is_alive = None
		self.hunger=0
		self.DIE_ON_EAT = die_on_eat

		self.add_walls = add_walls

		self.num_foods = num_foods

		self.obs_type = obs_type

		if obs_type == 'vector':
			self.vector=True
		else:
			self.vector=False
		self.arena = Arena(self.SIZE, num_snakes=num_snakes, num_foods=self.num_foods, walls=self.add_walls, vector=self.vector)

		self.obs_type = obs_type
		if self.obs_type == 'raw':
		    self.observation_space = spaces.Box(low=0, high=255, shape=(self.SIZE[0]*obs_zoom, self.SIZE[1]*obs_zoom), dtype=np.uint8)
		elif self.obs_type == 'rgb':
		    self.observation_space = spaces.Box(low=0, high=255, shape=(self.SIZE[0]*obs_zoom, self.SIZE[1]*obs_zoom, 3), dtype=np.uint8)
		    self.RGBify = RGBifier(self.SIZE, zoom_factor = obs_zoom, players_colors={})
		elif self.obs_type == 'layered':
		    # Only 2 layers here, food and snek
			self.observation_space = spaces.Box(low=0, high=255, shape=(self.SIZE[0]*obs_zoom, self.SIZE[1]*obs_zoom, 2), dtype=np.uint8)
		elif self.obs_type == 'vector':
			self.observation_space = spaces.Box(low=0, high=np.inf, shape=(10+self.num_foods,), dtype=np.uint8)
		else:
			raise(Exception('Unrecognized observation mode.'))

		self.action_space = spaces.Discrete(len(self.arena.DIRS))

		self.RENDER_ZOOM = render_zoom
		self.renderer = None

	def step(self, actions):
		if self.is_alive is None or not any (self.is_alive):
			raise Exception('Need to reset environment.')

		self.current_step += 1

		rewards, dones = self.arena.move_snake(actions)

		self.hunger = [h+1 if r <= 0 else 0 for h, r in zip(self.hunger, rewards)]

		self.is_alive = [not done for done in dones]
		return self._get_state(), rewards, dones, {}

	def reset(self):
		self.current_step = 0
		self.is_alive = [True] * self.num_snakes
		self.hunger = [0]*self.num_snakes

		self.arena = Arena(self.SIZE, num_snakes=self.num_snakes, num_foods=self.num_foods, walls=self.add_walls, vector=self.vector)
		return self._get_state()

	def seed(self, seed):
		random.seed(seed)

	def _get_state(self):
		state = self.arena.get_obs()
		if self.obs_type == 'rgb':
			return self.RGBify.get_image(state)
		elif self.obs_type == 'layered':
			s = np.array([(state == self.world.FOOD).astype(int), ((state == self.world.sneks[0].snek_id) or (state == self.world.sneks[0].snek_id+1)).astype(int)])
			s = np.transpose(s, [1, 2, 0])
			return s
		elif self.obs_type == 'raw':
			return self.arena.get_obs()
		elif self.obs_type == 'vector':
			return self.arena.get_obs()

	def render(self, mode='human', close=False):
		if not close:
			# Renderer lazy loading
			if self.renderer is None:
				self.renderer = Renderer(self.SIZE, zoom_factor = self.RENDER_ZOOM, players_colors={})
		return self.renderer._render(self.arena.render_obs(), mode=mode, close=False)
			
	def close(self):
		if self.renderer:
			self.renderer.close()
			self.renderer = None