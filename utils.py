import os

def load_env():
  if os.path.isfile('.env'):
    with open('.env') as f:
      for line in f:
        k, v = line.strip().split('=', 1)
        os.environ[k] = v