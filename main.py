from src.environment.warehouse_env import WarehouseEnv

if __name__ == '__main__':
    env = WarehouseEnv(mode='NORMAL')
    env.run()
