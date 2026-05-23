from src.environment.warehouse_env import WarehouseEnv

MODES = [
    'NORMAL',
    'STRESS_TEST',
    'FAILURE_CONDITIONS',
    'SCALABILITY',
    'EXTREME_LOAD'
]

for m in MODES:
    print('RUNNING:', m)
    env = WarehouseEnv(mode=m)
    env.run()
