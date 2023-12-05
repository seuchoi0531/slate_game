import gym




def main():
    env = gym.make('SlateGameEnv-v0')
    observation = env.reset()
    
    for _ in range(1000):
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)

        if done:
            observation = env.reset()

if __name__ == '__main__':
    main()