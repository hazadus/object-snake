class Block:
    """
    Базовый класс, описывающий минимальный элемент игрового поля - блок.

    __x: координата х блока на поле (в блоках)
    __y: координата y блока на поле (в блоках)

    Args:
        x (int): передаётся координата х блока на поле (в блоках)
        y (int): передаётся координата y блока на поле (в блоках)
    """
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    def x(self) -> int:
        """
        Геттер координаты x блока на игровом поле.

        :return: __x
        :rtype: int
        """
        return self.__x

    def set_x(self, new_x: int) -> int:
        """
        Сеттер координаты x блока на игровом поле.

        :param new_x: Новая координата х блока.
        :return: Предыдущее значение координаты х блока.
        """
        prev_x = self.__x
        self.__x = new_x
        return prev_x

    def y(self) -> int:
        """
        Геттер координаты y блока на игровом поле.

        :return: __y
        :rtype: int
        """
        return self.__y

    def set_y(self, new_y) -> int:
        """
        Сеттер координаты y блока на игровом поле.

        :param new_y: Новая координата y блока.
        :return: Предыдущее значение координаты y блока.
        """
        prev_y = self.__y
        self.__y = new_y
        return prev_y

    def __eq__(self, other):
        return self.__x == other.__x and self.__y == other.__y


class Food(Block):
    """
    Описывает подвид блока - еду для змейки.

    __points: количество очков, начисляемое при поедании змейкой данной еды.

    Args:
        block (Block): инстанс блока, на месте которого создаётся инстанс еды.
    """
    def __init__(self, block: Block):
        Block.__init__(self, block.x(), block.y())
        self.__points = 10

    def points(self) -> int:
        """
        Возвращает количество очков, начисляемое при поедании змейкой данной еды.

        :return: __points
        """
        return self.__points


class SnakeBlock(Block):
    """
    Описывает подвид блока – элемент змейки.

    Args:

    """
    def __init__(self, x, y, is_head=False, next_block=None):
        """
        :param x: координата в блоках
        :param y: координата в блоках
        """
        Block.__init__(self, x, y)
        self.is_head = is_head
        self.next_block = next_block
