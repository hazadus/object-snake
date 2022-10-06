class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Food(Block):
    points = 10


class SnakeBlock(Block):
    def __init__(self, x, y, is_head=False, next_block=None):
        """
        :param x: координата в блоках
        :param y: координата в блоках
        """
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.is_head = is_head
        self.next_block = next_block
