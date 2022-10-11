from datetime import datetime
import logging
import pickle


class Score:
    """
    Описывает одну запись в таблице рекордов.

    __name: имя игрока
    __score: счет игры
    __date_added: дата и время записи

    Args:
        name (str): имя игрока
        score (int): счет игры
        date_added (datetime): дата и время записи

    """
    def __init__(self, name: str, score: int, date_added=datetime.now()):
        self.__name = name
        self.__score = score
        self.__date_added = date_added

    def score(self) -> int:
        """
        Значение счета в данной записи.

        :return: __score
        """
        return self.__score

    def set_date_added(self, new_datetime: datetime):
        """
        Установить дату добавления записи в соответствии с переданной.

        :param new_datetime: дата и время для установки в записи
        """
        self.__date_added = new_datetime

    def __repr__(self):
        return f'{self.__name} {self.__score} {self.__date_added.strftime("%d.%m.%Y %H:%M")}'


class Highscores:
    """
    Описывает таблицу рекордов, в которой хранятся записи обо всех результатах игр. Сохраняется в объекте pickle.
    Данные из файла загружаются при создании инстанса!
    """
    def __init__(self):
        self.__highscores_filename = 'highscores.pkl'
        self.__scores = list()
        self.load()

    def add(self, new_score: Score):
        """
        Добавляет новую запись о результатах игры в список.

        :param new_score: запись для добавления
        """
        new_score.set_date_added(datetime.now())
        self.__scores.append(new_score)

    def get_all(self):
        """
        Возвращает отсортированный по убыванию полный список записей о результатах игр.

        :return: отсортированный по убыванию полный список записей о результатах игр состоящих из инстансов Score
        """
        return sorted(self.__scores, key=lambda x: x.score(), reverse=True)

    def load(self):
        """
        Загружает записи из файла pickle.
        """
        try:
            with open(self.__highscores_filename, 'rb') as file:
                self.__scores = pickle.load(file)
                logging.info(f'Highscores loaded from "{self.__highscores_filename}".')
        except FileNotFoundError:
            logging.info(f'File "{self.__highscores_filename}" not found.')

    def save(self):
        """
        Сохраняет записи в файле pickle.
        """
        # noinspection PyBroadException
        try:
            with open(self.__highscores_filename, 'wb') as file:
                pickle.dump(self.__scores, file)
                logging.info(f'Highscores saved to "{self.__highscores_filename}".')
        except:
            logging.info(f'An error has occured while trying to save to "{self.__highscores_filename}".')


if __name__ == '__main__':
    """
    При запуске данного модуля – вывести таблицу рекордов.
    """
    hs = Highscores()
    for i, i_score in enumerate(hs.get_all()):
        print(f'{i + 1}. {i_score}')
