class SnakeBlock:
    def __init__(self, x, y, is_head=False):
        """
        :param x: координата в блоках
        :param y: координата в блоках
        """
        self.x = x
        self.y = y
        self.is_head = is_head


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

    def make_move(self):
        dx, dy = self.direction
        if self.head.x == 0 and dx < 0:
            pass
        else:
            self.head.x += dx

        if self.head.y == 0 and dy < 0:
            pass
        else:
            self.head.y += dy
