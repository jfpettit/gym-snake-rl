import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import random

from core_snake import Snake, Arena
from render import Renderer, RGBifier

class SingleSnake(gym.Env):
	metadata = {
	'render.modes' : ['human', 'rgb_array'],
	'observation.types' : ['vector', 'raw', 'rgb', 'layered']
	}
	def __init__(self, size=(15, 15), step_limit=1000, dynamic_step_limit=1000, obs_type='vector', obs_zoom=1, num_foods=1,
	 die_on_eat=False, render_zoom=20, add_walls=False):
		self.SIZE=size
		self.STEP_LIMIT = step_limit
		self.DYNAMIC_STEP_LIMIT = dynamic_step_limit

		self.hunger=0
		self.DIE_ON_EAT = die_on_eat

		self.add_walls = add_walls

		self.num_foods = num_foods

		if obs_type == 'vector':
			self.vector=True
		else:
			self.vector=False
		self.arena = Arena(self.SIZE, num_foods=self.num_foods, walls=self.add_walls, vector=self.vector)

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
			self.observation_space = spaces.Box(low=0, high=np.inf, shape=(10*self.num_foods,), dtype=np.uint8)
		else:
			raise(Exception('Unrecognized observation mode.'))

		self.action_space = spaces.Discrete(len(self.arena.DIRS))

		self.RENDER_ZOOM = render_zoom
		self.renderer = None

	def step(self, action):
		if not self.is_alive:
			raise Exception('Need to reset env.')

		self.current_step += 1
		if self.current_step >= self.STEP_LIMIT or self.hunger > self.DYNAMIC_STEP_LIMIT:
			self.is_alive = False
			return self._get_state(), 0, True, {}

		rewards, dones = self.arena.move_snake(action)

		self.hunger += 1
		if rewards[0] > 0:
			self.hunger = 0

		if rewards[0] > 0 and self.DIE_ON_EAT:
			dones[0] = True

		if dones[0]:
			self.is_alive = False
		return self._get_state(), rewards[0], dones[0], {}

	def reset(self):
		self.current_step = 0
		self.hunger = 0
		self.is_alive = True

		self.arena = Arena(self.SIZE, num_foods=self.num_foods, walls=self.add_walls, vector=self.vector)
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


