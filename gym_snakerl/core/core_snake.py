import numpy as np
import random
from scipy.spatial.distance import euclidean
import warnings

class Snake:
    DIRS = [np.array([-1,0]), np.array([0,1]), np.array([1,0]), np.array([0,-1])]
    def __init__(self, identification, start_position, start_position_idx, start_len):
        self.current_position_idx = start_position_idx
        self.snake_id = identification
        self.is_alive = True
        self.body = [start_position]
        current_loc = np.array(start_position)
        for i in range(1, start_len):
            current_loc = current_loc - self.DIRS[start_position_idx]
            self.body.append(tuple(current_loc))

    def grow(self, loc):
        self.body.append(tuple(loc))

    def check_action_ok(self, action):
        return (action != self.current_position_idx) and (action != (self.current_position_idx+2)%len(self.DIRS))

    def step(self, action):
        if self.check_action_ok(action):
            self.current_position_idx = action

        tail = self.body[-1]
        if len(self.body) > 1:
            self.body = self.body[:-1]
        
        updated_head = np.array(self.body[0] + self.DIRS[self.current_position_idx])

        self.body = [tuple(updated_head)] + self.body

        return tuple(updated_head), tail

class Arena:
    DIRS = [np.array([-1,0]), np.array([0,1]), np.array([1,0]), np.array([0,-1])]
    def __init__(self, size=(15, 15), num_snakes=1, num_foods=1, num_obstacles=None, add_walls=False, vector=True, rew_func=None, block_size_limit=None):
        self.die_reward = -1.
        self.move_reward = 0.
        self.eat_reward = 1.
        if rew_func is not None:
            self.die_reward = rew_func[0]
            self.move_reward = rew_func[1]
            self.eat_reward = rew_func[2]

        self.food = 64
        self.wall = 255
        self.vector = vector

        self.num_snakes = num_snakes
        self.num_foods = num_foods

        self.size = size
        self.arena = np.zeros(self.size)
        self.add_walls = add_walls

        if add_walls:
            self.arena[0, :] = self.wall
            self.arena[:, 0] = self.wall
            self.arena[-1, :] = self.wall
            self.arena[:, -1] = self.wall

        self.available_posns = set(zip(*np.where(self.arena == 0)))

        self.snakes = []
        self.food_locs = []
        for _ in range(num_snakes):
            snake = self.register_snake()

        self.put_food(num_foods = num_foods)

        if num_obstacles is not None:
            self.block_size_limit = block_size_limit
            self.num_obstacles = num_obstacles
            self.randomize_map()

    def randomize_map(self):
        self.snakes=[]
        self.food_locs=[]
        self.arena = np.zeros(self.size)
        if self.add_walls:
            self.arena[0, :] = self.wall
            self.arena[:, 0] = self.wall
            self.arena[-1, :] = self.wall
            self.arena[:, -1] = self.wall
        
        if self.num_obstacles > max(self.size)//3: 
                warnings.warn('You may have set your num_obstacles too high for your current arena size. If issues arise, try increasing the size of your arena or decreasing your num_obstacles.')
        if self.block_size_limit is None:
            self.block_size_limit = min(self.size)//3
        else:
            self.block_size_limit=self.block_size_limit
            if self.block_size_limit > min(self.size)//2:
                warnings.warn('You may have set your block_size_limit too high for your current arena size. If issues arise, try increasing the size of your arena or decreasing your block_size_limit.')
        for i in range(self.num_obstacles):
            a = random.choice(range(1, self.size[0]))
            b = random.choice(range(1, self.size[1]))
            asub_val = random.choice(list(range(self.block_size_limit)))
            bsub_val = random.choice(list(range(self.block_size_limit)))
            self.arena[a-asub_val:a, b-bsub_val:b] = 255

        for j in range(2):
            for i in range(1, len(self.arena)-1):
                for j in range(1, len(self.arena[i])-1):
                    above = self.arena[i-1, j]
                    below = self.arena[i+1, j]
                    left = self.arena[i, j-1]
                    right = self.arena[i, j+1]
                    aboveleft = self.arena[i-1, j-1]
                    aboveright = self.arena[i-1, j+1]
                    belowleft = self.arena[i+1, j-1]
                    belowright=self.arena[i+1, j+1]
                    val = [above, below, left, right, aboveleft, aboveright, belowleft, belowright]
                    if sum(val) >= 5 * 255:
                        self.arena[i, j] = 255

            for i in range(len(self.arena)-2, 0, -1):
                for j in range(len(self.arena[i])-2, 0, -1):
                    above = self.arena[i-1, j]
                    below = self.arena[i+1, j]
                    left = self.arena[i, j-1]
                    right = self.arena[i, j+1]
                    aboveleft = self.arena[i-1, j-1]
                    aboveright = self.arena[i-1, j+1]
                    belowleft = self.arena[i+1, j-1]
                    belowright=self.arena[i+1, j+1]
                    val = [above, below, left, right, aboveleft, aboveright, belowleft, belowright]
                    if sum(val) >= 5 * 255:
                        self.arena[i, j] = 255
        self.available_posns = set(zip(*np.where(self.arena == 0)))
        for _ in range(self.num_snakes):
            self.register_snake()
        self.put_food(num_foods=self.num_foods)

    def register_snake(self):
        snakesize = 1
        position = random.choice(list(self.available_posns))
        while position in self.snakes:
            position = random.choice(list(self.available_posns))

        start_direction_idxs = [Snake.DIRS[0], Snake.DIRS[1], Snake.DIRS[2], Snake.DIRS[3]]
        #new_snakes = [Snake(100 + 2 * len(self.snakes), position, i, snakesize) for i in range(len(start_direction_idxs))]
        
        #if len(new_snakes) == 0:
        #   for i in range(100):
        #       position = random.choice(list(self.available_posns))
        #       while position in self.snakes:
        #           position = random.choice(list(self.available_posns))

        #       start_direction_idxs = [Snake.DIRS[0], Snake.DIRS[1], Snake.DIRS[2], Snake.DIRS[3]]
        #       new_snakes = [Snake(100 + 2 * len(self.snakes), position, i, snakesize) for i in range(len(start_direction_idxs))]
        #       for i in range(len(new_snakes)):
        #           for j in range(len(new_snakes[i].body)):
        #               if self.arena[new_snakes[i].body[j][0], new_snakes[i].body[j][1]] == 255:
        #                   del(i)
        #       if len(new_snakes) != 0:
        #           break
        start_direction_idx = random.randrange(len(start_direction_idxs))
        new_snake = Snake(100 + 2 * len(self.snakes), position, start_direction_idx, snakesize)
        self.snakes.append(new_snake)
        return new_snake

    def get_alive_snakes(self):
        return [snake for snake in self.snakes if snake.is_alive]

    def put_food(self, num_foods):
        available_posns = self.available_posns

        for snake in self.get_alive_snakes():
            available_posns -= set(snake.body)

        for _ in range(num_foods):
            pos_choice = random.choice(list(available_posns))
            while self.arena[pos_choice[0], pos_choice[1]] != 0:
                pos_choice = random.choice(list(available_posns))
            self.arena[pos_choice[0], pos_choice[1]] = self.food
            self.food_locs.append(pos_choice)
            available_posns.remove(pos_choice)

    def render_obs(self):
        obs = self.arena.copy()

        for snake in self.get_alive_snakes():
            for part in snake.body:
                obs[part[0], part[1]] = snake.snake_id
            obs[snake.body[0][0], snake.body[0][1]] = snake.snake_id + 10
        return obs

    def get_obs(self):
        obs = []
        # include squares around head for observations. Nothing crazy, but enough to be able to see if it is
        # going to hit itself or another snake or a wall. So like being able to see one square around itself
        if self.vector:
            for snake in self.get_alive_snakes():
                hl1, hl2 = snake.body[0][0], snake.body[0][1]

                around_head = (self.arena[hl1+1, hl2-1], self.arena[hl1+1, hl2], self.arena[hl1+1, hl2+1],
                    self.arena[hl1, hl2-1], self.arena[hl1, hl2], self.arena[hl1, hl2 + 1])
                length = len(snake.body)
                #dist_from_food = np.array([euclidean(snake.body[0], i) for i in self.food_locs]).mean()
                dist_from_food = np.array([euclidean(snake.body[0], i) for i in self.food_locs])
                obs.append((*around_head, length, *dist_from_food))
            return obs
        else:
            return self.render_obs()

    def check_in_bounds(self, loc):
        return not (0 <= loc[0] < self.size[0]) or not(0 <= loc[1] < self.size[1]) or self.arena[loc[0], loc[1]] == self.wall

    def move_snake(self, actions):
        rewards = [0] * len(self.snakes)
        dones = []
        new_food_needed = 0
        for i, (snake, action) in enumerate(zip(self.snakes, actions)):
            if not snake.is_alive:
                continue
            new_snake_head, old_snake_tail = snake.step(action)
            if self.check_in_bounds(new_snake_head):
                snake.body = snake.body[1:]
                snake.is_alive = False
            elif new_snake_head in snake.body[1:]:
                snake.is_alive = False
            for j, other_snake in enumerate(self.snakes):
                if i != j and other_snake.is_alive:
                    if new_snake_head == other_snake.body[0]:
                        snake.is_alive = False
                        other_snake.is_alive = False
                    elif new_snake_head in other_snake.body[1:]:
                        snake.is_alive = False
            if snake.is_alive and self.arena[new_snake_head[0], new_snake_head[1]] == self.food:
                self.arena[new_snake_head[0], new_snake_head[1]] = 0

                snake.body.append(old_snake_tail)

                new_food_needed += 1
                rewards[i] = self.eat_reward

            elif snake.is_alive:
                rewards[i] = self.move_reward

        dones = [not snake.is_alive for snake in self.snakes]
        rewards = [r if snake.is_alive else self.die_reward for r, snake in zip(rewards, self.snakes)]

        if new_food_needed > 0:
            self.put_food(num_foods=new_food_needed)
        return rewards, dones






