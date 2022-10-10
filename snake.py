import random
import logging

from blocks import Food, SnakeBlock


class Snake:
    """
    Класс описывает змейку, состоящую из блоков SnakeBlock. Изначально змейка состоит только из одного блока - головы.
    Направление движения выбирается случайно.

    __head (SnakeBlock): головной блок змейки
    __blocks (list): список всех блоков в змейке
    __direction (tuple): направление движения змейки
    __prev_direction (tuple): направление движения змейки в предыдущий "ход"

    Args:
        x (int): Координата x головного блока змейки на игровом поле (в блоках)
        y (int): Координата y головного блока змейки на игровом поле (в блоках)
    """
    direction_right = (1, 0)
    direction_left = (-1, 0)
    direction_up = (0, -1)
    direction_down = (0, 1)
    all_directions = tuple([direction_right, direction_left, direction_up, direction_down])
    opposite_directions = tuple(
        [
            (direction_right, direction_left), (direction_left, direction_right),
            (direction_up, direction_down), (direction_down, direction_up)
        ]
    )

    def __init__(self, x, y):
        self.__head = SnakeBlock(x=x, y=y, is_head=True)
        self.__blocks = list()
        self.__blocks.append(self.__head)
        self.__direction = self.__prev_direction = random.choice(self.all_directions)

    def __len__(self) -> int:
        """
        Возвращает длину змейки в блоках.

        :return: len(self.blocks())
        """
        return len(self.blocks())

    def head(self) -> SnakeBlock:
        """
        Возвращает головной блок змейки.

        :return: __head
        """
        return self.__head

    def set_head(self, new_head: SnakeBlock):
        """
        Устанавливает головной блок змейки.

        :param new_head: новый блок для головы
        """
        self.__head = new_head

    def blocks(self) -> tuple:
        """
        Возвращает кортеж всех блоков, из которых состоит змейка.

        :return: tuple(self.__blocks)
        """
        return tuple(self.__blocks)

    def set_direction(self, new_direction: tuple):
        """
        Устанавливает передаваемое направление движения, если оно не противоположно направлению в предыдущий ход -
        змейка не может двигаться назад! В противном случае направление движения не меняется.

        :param new_direction: кортеж направления вида (dx, dy)
        :raise ValueError: если направление не является одним из описанных в Snake.all_directions
        """
        if new_direction not in self.all_directions:
            raise ValueError(f'Wrong direction passed - {new_direction}')
        if (new_direction, self.get_prev_direction()) not in self.opposite_directions:
            self.__direction = new_direction

    def eat(self, food: Food) -> int:
        """
        Описывает поглощение инстанса еды змейкой. Блок еды превращается в голову змейки, бывшая голова перестает быть
        таковой и присоединяется к новой вместе с остальным "хвостом", присоединенный блок добавляется в список всех
        блоков в змейке.

        :param food: инстанс еды для поглощения
        :return: количество очков, заработанных за поглощение данного инстанса еды
        """
        self.head().set_as_head(is_head=False)
        new_head = SnakeBlock(x=food.x(), y=food.y(), is_head=True, next_block=self.head())
        self.set_head(new_head)
        self.__blocks.append(new_head)
        logging.info(f'Ate food at: ({food.x()}, {food.y()})')
        return food.points()

    def kill(self):
        """
        Уничтожает змейку, стирая все её блоки из списка.

        """
        self.__head = None
        self.__blocks.clear()

    def move_to(self, new_x: int, new_y: int):
        """
        Двигает змейку по цепочке в указанную точку поля "не думая", все проверки коллизий проводятся в классе Board.
        Передвижение змейки - это один её "ход" на игровом поле.
        Также сохраняется направление движения в данный ход как "предыдущее" для дальнейших проверок возможности смены
        направления (змейка не может двигаться назад!).

        :param new_x: координата x блока на поле, куда должна переместиться голова змейки
        :param new_y: координата y блока на поле, куда должна переместиться голова змейки
        """
        prev_x = self.head().x()
        self.head().set_x(new_x)
        prev_y = self.head().y()
        self.head().set_y(new_y)

        next_block = self.head().next_block()
        while next_block is not None:
            curr_block = next_block
            prev_x = curr_block.set_x(prev_x)
            prev_y = curr_block.set_y(prev_y)
            next_block = curr_block.next_block()

        self.__prev_direction = self.__direction

    def predict_head_position(self) -> tuple:
        """
        Предсказывает координаты головы змейки на игровом поле в следующий ход с учетом направления движения змейки.

        :return: кортеж координат вида (x, y) в блоках.
        """
        dx, dy = self.__direction
        return self.head().x() + dx, self.head().y() + dy

    def get_prev_direction(self):
        """
        Возвращает направление движения змейки в прошлый ход.

        :return: кортеж направления вида (dx, dy)
        """
        return self.__prev_direction

    def can_set_direction(self, new_direction):
        """
        Проверить, может ли змейка двигаться в этом нарпавлении.

        :param new_direction:
        :return:
        """
        pass
