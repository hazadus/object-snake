import sys
import logging

from game import Game
from engine import Engine


logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("object-snake.log"),
        logging.StreamHandler(sys.stdout)  # output to file AND console
    ],
    format="%(asctime)s | %(levelname)s | %(module)s/%(funcName)s():%(lineno)d - %(message)s",
    datefmt='%d/%m/%Y %H:%M:%S',
    )

logging.info('Hello')

if __name__ == '__main__':
    engine = Engine(Game(40, 40), 'Objective Snake')
    engine.game_loop()
    engine.quit()
