from food import Food


class SnakeBlock:
    def __init__(self, x, y, is_head=False, next_block=None):
        """
        :param x: координата в блоках
        :param y: координата в блоках
        """
        self.x = x
        self.y = y
        self.is_head = is_head
        self.next_block = next_block


class Snake:
    blocks = []
    direction_right = (1, 0)
    direction_left = (-1, 0)
    direction_up = (0, 1)
    direction_down = (0, -1)
    direction_stopped = (0, 0)
    direction = direction_stopped

    # speed
    # grow()
    def __init__(self, x, y):
        block = SnakeBlock(x, y, True)
        self.head = block
        self.blocks.append(block)

    def set_direction(self, new_direction: tuple):
        self.direction = new_direction

    def eat(self, food: Food):
        self.head.is_head = False
        new_head = SnakeBlock(food.x, food.y, True, self.head)
        self.head = new_head
        self.blocks.append(new_head)

    def make_move(self):
        dx, dy = self.direction
        moved = False
        if self.head.x == 0 and dx < 0:
            pass
        else:
            prev_x = self.head.x
            self.head.x += dx
            moved = True

        if self.head.y == 0 and dy < 0:
            pass
        else:
            prev_y = self.head.y
            self.head.y += dy
            moved = True

        if moved:
            next_block = self.head.next_block
            while next_block is not None:
                curr_block = next_block
                curr_block.x, prev_x = prev_x, curr_block.x
                curr_block.y, prev_y = prev_y, curr_block.y
                next_block = curr_block.next_block

    def predict_head_position(self) -> tuple:
        dx, dy = self.direction
        return self.head.x + dx, self.head.y + dy
