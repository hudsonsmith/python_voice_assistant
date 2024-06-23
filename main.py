from config import Config
from src.bot import Bot

if __name__ == "__main__":
    b: Bot = Bot(Config.name)
    print(b)
    b.run()
