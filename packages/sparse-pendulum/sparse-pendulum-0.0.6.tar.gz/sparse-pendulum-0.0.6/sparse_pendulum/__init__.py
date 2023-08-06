from gym.envs.registration import register

register(
    id='SparsePendulum-v0',
    entry_point='sparse_pendulum.envs:SparsePendulumEnv',
    kwargs={
        'max_speed': 8,
        'max_torque': 2.0,
        'reward_angle_limit':5.0,
        'reward_speed_limit':2.0,
        'balance_counter': 5,
        'reward_mode': 'binary'
    }

)
