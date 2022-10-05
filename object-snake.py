from game import Game
from engine import Engine


if __name__ == '__main__':
    engine = Engine(Game(40, 40), 'Objective Snake')
    engine.game_loop()
    engine.quit()
