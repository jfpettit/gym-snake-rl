from gym.envs.registration import register
import itertools

VERSION = '-v0'

SETTINGS = {
    'ENV_TYPE': [
        ('BasicSnake', {'entry_point': 'gym_snake_rl.envs:SingleSnake'}),
        ('BasicSnakePBRS', {'entry_point': 'gym_snake_rl.envs:SingleSnake', 'potential_based_rewards' : True}),
        ('HungrySnake', {'dynamic_step_limit': 100, 'entry_point': 'gym_snake_rl.envs:SingleSnake'}),
        ('HungrySnakePBRS', {'dynamic_step_limit': 100, 'entry_point': 'gym_snake_rl.envs:SingleSnake', 'potential_based_rewards' : True}),
        ('BabySnake', {'die_on_eat' : True, 'entry_point': 'gym_snake_rl.envs:SingleSnake'}),
        ('BabySnakePBRS', {'die_on_eat' : True, 'entry_point': 'gym_snake_rl.envs:SingleSnake', 'potential_based_rewards' : True}),
        ('TwoSnakesOneFood', {'entry_point': 'gym_snake_rl.envs:MultiSnake', 'num_snakes': 2}),
        ('ThreeSnakesOneFood', {'entry_point': 'gym_snake_rl.envs:MultiSnake', 'num_snakes': 3}),
        ('TenSnakesOneFood', {'entry_point': 'gym_snake_rl.envs:MultiSnake', 'num_snakes': 10}),
        ('ObstacleBasicSnake', {'entry_point' : 'gym_snake_rl.envs:SingleSnake', 'num_obstacles' : 8}),
        ('ObstacleBasicSnakePBRS', {'entry_point' : 'gym_snake_rl.envs:SingleSnake', 'num_obstacles' : 8, 'potential_based_rewards' : True}),
        ('ObstacleTwoSnakesOneFood', {'entry_point' : 'gym_snake_rl.envs:MultiSnake', 'num_obstacles' : 7, 'num_snakes' : 2}),
        ('ObstacleThreeSnakesOneFood', {'entry_point' : 'gym_snake_rl.envs:MultiSnake', 'num_obstacles' : 7, 'num_snakes' : 3}),
        ('ObstacleTenSnakesOneFood', {'entry_point':'gym_snake_rl.envs:MultiSnake', 'num_obstacles' : 4, 'num_snakes' : 10}),
        ('ObstacleHungrySnake', {'dynamic_step_limit' : 100, 'entry_point' : 'gym_snake_rl.envs:SingleSnake', 'num_obstacles' : 8}),
        ('ObstacleHungrySnakePBRS', {'dynamic_step_limit' : 100, 'entry_point' : 'gym_snake_rl.envs:SingleSnake', 'num_obstacles' : 8, 'potential_based_rewards' : True}), 
        ('TwoSnakesTwoFoods', {'entry_point': 'gym_snake_rl.envs:MultiSnake', 'num_snakes': 2, 'num_foods':2}),
        ('ThreeSnakesThreeFoods', {'entry_point': 'gym_snake_rl.envs:MultiSnake', 'num_snakes': 3, 'num_foods' : 3}),
        ('TenSnakesTenFoods', {'entry_point': 'gym_snake_rl.envs:MultiSnake', 'num_snakes': 10, 'num_foods' : 10}),
        ('ObstacleTwoSnakesTwoFoods', {'entry_point' : 'gym_snake_rl.envs:MultiSnake', 'num_obstacles' : 7, 'num_snakes' : 2, 'num_foods' : 2}),
        ('ObstacleThreeSnakesThreeFoods', {'entry_point' : 'gym_snake_rl.envs:MultiSnake', 'num_obstacles' : 7, 'num_snakes' : 3, 'num_foods' : 3}),
        ('ObstacleTenSnakesTenFoods', {'entry_point':'gym_snake_rl.envs:MultiSnake', 'num_obstacles' : 4, 'num_snakes' : 10, 'num_foods' : 10}),
    ],
    'SIZES': [
        ('-16', {'size': (16, 16)}),
        ('-32', {'size': (32, 32)}),
        ('-64', {'size': (64, 64)}),
    ],
    'OBSERVATION_TYPES': [
        ('-raw', {'obs_type': 'raw', 'obs_zoom': 1}),
        ('-rgb', {'obs_type': 'rgb', 'obs_zoom': 1}),
        ('-rgb5', {'obs_type': 'rgb', 'obs_zoom': 5}),
        ('-small_vector', {'obs_type': 'small_vector', 'obs_zoom' : 1}),
        ('-big_vector', {'obs_type' : 'big_vector', 'obs_zoom' : 1})
    ],
    'WALLS': [
        ('', {'add_walls': True}),
        #('-NoWalls', {'add_walls': False})
    ]
}
# Settings key, also fix the order of options
SETTINGS_KEY = ['ENV_TYPE', 'OBSERVATION_TYPES', 'SIZES', 'WALLS']

for setting_index in itertools.product(*[range(len(SETTINGS[key])) for key in SETTINGS_KEY]):
    # Get the setting
    env_id = ''
    setting = {}
    for i, key in enumerate(SETTINGS_KEY):
        # Get the label and settings dict
        label, value = SETTINGS[key][setting_index[i]]
        # Add to label
        env_id += label
        # Add to settings dict
        setting = {**setting, **value}
    # Add version to id
    env_id += VERSION
    # Save entrypoint and remove from settings
    entry_point = setting['entry_point']
    setting.pop('entry_point', None)
    # Register the environment
    register(
        id=env_id,
        entry_point=entry_point,
        kwargs = setting
)