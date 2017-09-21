from gym.envs.registration import register

register(
    id='dc4-v0',
    entry_point='gym_dc4.gym_dc4.envs:DC4Env'
)
register(
    id='dc4-extrahard-v0',
    entry_point='gym_dc4.envs:dc4ExtraHardEnv'
)