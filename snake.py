import logging

from blocks import Food, SnakeBlock


class Snake:
    direction_right = (1, 0)
    direction_left = (-1, 0)
    direction_up = (0, -1)
    direction_down = (0, 1)
    direction_stopped = (0, 0)

    def __init__(self, x, y):
        block = SnakeBlock(x, y, True)
        self.head = block
        self.blocks = list()
        self.blocks.append(block)
        self.__direction = self.__prev_direction = self.direction_right

    def set_direction(self, new_direction: tuple):
        self.__prev_direction = self.__direction
        self.__direction = new_direction

    def eat(self, food: Food):
        self.head.is_head = False
        new_head = SnakeBlock(food.x(), food.y(), True, self.head)
        logging.info(f'Ate food at: ({food.x()}, {food.y()})')
        self.head = new_head
        self.blocks.append(new_head)

    def kill(self):
        while self.blocks:
            self.blocks.pop()

    def move_to(self, new_x, new_y):
        """
        Двигает змейку в указанную точку "не думая", все проверки коллизий в классе Board.
        :param new_x:
        :param new_y:
        :return:
        """
        prev_x = self.head.x()
        self.head.set_x(new_x)
        prev_y = self.head.y()
        self.head.set_y(new_y)

        next_block = self.head.next_block()
        while next_block is not None:
            curr_block = next_block
            prev_x = curr_block.set_x(prev_x)
            prev_y = curr_block.set_y(prev_y)
            next_block = curr_block.next_block()

        self.__prev_direction = self.__direction

    def predict_head_position(self) -> tuple:
        dx, dy = self.__direction
        return self.head.x() + dx, self.head.y() + dy

    def get_prev_direction(self):
        return self.__prev_direction
