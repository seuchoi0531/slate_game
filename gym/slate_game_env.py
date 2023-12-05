import gym
from gym import spaces
import numpy as np
from gym.envs.registration import register

class SlateGameEnv(gym.Env):
    def __init__(self):
        super(SlateGameEnv, self).__init__()
        
        low_boolean = np.zeros((6, 6), dtype=np.int)
        high_boolean = np.ones((6, 6), dtype=np.int)
        shape_boolean = (6, 6)
        dtype_boolean = np.int

        low_integers = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int)
        high_integers = np.array([4, 10, 4, 10, 4, 4, 4, 10, 5, 5, 3], dtype=np.int)

        low = np.concatenate([low_boolean.flatten(), low_integers])
        high = np.concatenate([high_boolean.flatten(), high_integers])
        shape = shape_boolean + (len(low_integers),)
        dtype = [dtype_boolean, np.int]

        self.action_sapce = spaces.Discrete(72)
        self.observation_space = spaces.Tuple((
            spaces.Box(low=low_boolean, high=high_boolean, shape=shape_boolean, dtype=dtype_boolean),
            spaces.Box(low=low_integers, high=high_integers, shape=(len(low_integers),), dtype=np.int)
        ))

    def reset(self):
        pass

    def step(self, action):
        pass



register(
    id='SlateGameEnv-v0',
    entry_point='slate_game_env:SlateGameEnv'
)