from openreward.environments import Server

from env import TowerOfHanoiEnvironment

if __name__ == "__main__":
    server = Server([TowerOfHanoiEnvironment])
    server.run()
