import sys
import logging

from engine import Engine
from config import Config


# Инициализируем логгер в первую очередь, т.к. он используется во всех классах игры
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler('object-snake.log'),
        logging.StreamHandler(sys.stdout)  # output to file AND console
    ],
    format="%(asctime)s | %(levelname)s | %(module)s/%(funcName)s():%(lineno)d - %(message)s",
    datefmt='%d/%m/%Y %H:%M:%S',
    )

# Загружаем параметры из TOML-файла
config = Config('config.toml')

# Запускаем игру
engine = Engine(config=config)
engine.game_loop()
engine.quit()
