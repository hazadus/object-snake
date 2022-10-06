import logging

from blocks import Food, SnakeBlock


class Snake:
    blocks = []
    direction_right = (1, 0)
    direction_left = (-1, 0)
    direction_up = (0, -1)
    direction_down = (0, 1)
    direction_stopped = (0, 0)
    direction = direction_stopped

    def __init__(self, x, y):
        block = SnakeBlock(x, y, True)
        self.head = block
        self.blocks.append(block)

    def set_direction(self, new_direction: tuple):
        self.direction = new_direction

    def eat(self, food: Food):
        self.head.is_head = False
        new_head = SnakeBlock(food.x, food.y, True, self.head)
        logging.info(f'Ate food at: ({food.x}, {food.y})')
        self.head = new_head
        self.blocks.append(new_head)

    def move_to(self, new_x, new_y):
        """
        Двигает змейку в указанную точку "не думая", все проверки коллизий в классе Board.
        :param new_x:
        :param new_y:
        :return:
        """
        prev_x = self.head.x
        self.head.x = new_x
        prev_y = self.head.y
        self.head.y = new_y

        next_block = self.head.next_block
        while next_block is not None:
            curr_block = next_block
            curr_block.x, prev_x = prev_x, curr_block.x
            curr_block.y, prev_y = prev_y, curr_block.y
            next_block = curr_block.next_block

    def predict_head_position(self) -> tuple:
        dx, dy = self.direction
        return self.head.x + dx, self.head.y + dy
