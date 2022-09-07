import gym
import numpy as np
import pygame.time
import retro


class Discretizer(gym.ActionWrapper):

    def reverse_action(self, action):
        pass

    def __init__(self, env, combos):
        super().__init__(env)
        assert isinstance(env.action_space, gym.spaces.MultiBinary)
        buttons = env.unwrapped.buttons
        self._decode_discrete_action = []
        for combo in combos:
            arr = np.array([False] * env.action_space.n)
            for button in combo:
                arr[buttons.index(button)] = True
            self._decode_discrete_action.append(arr)

        self.action_space = gym.spaces.Discrete(len(self._decode_discrete_action))

    def action(self, act):
        return self._decode_discrete_action[act].copy()


class SuperMarioBrosDiscretizer(Discretizer):
    def __init__(self, env):
        super().__init__(env=env, combos=[['LEFT'], ['RIGHT'], ['A'], ['A', 'LEFT'], ['A', 'RIGHT']])


def main():
    env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
    env = SuperMarioBrosDiscretizer(env)
    print(env.buttons)

    env.reset()

    while True:
        action = env.action_space.sample()
        action = 3
        env.step(4)
        env.step(4)
        env.step(4)
        env.render()

        pygame.time.Clock().tick(60)


if __name__ == '__main__':
    main()
