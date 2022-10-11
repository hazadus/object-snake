from datetime import datetime
import logging
import pickle


class Score:
    def __init__(self, name: str, score: int, date_added=datetime.now()):
        self.name = name
        self.score = score
        self.date_added = date_added

    def __repr__(self):
        return f'{self.name} {self.score} {self.date_added.strftime("%d.%m.%Y %H:%M")}'


class Highscores:
    """
    Данные из файла загружаются при создании инстанса!
    """
    __highscores_filename = 'highscores.pkl'
    __scores = list()

    def __init__(self):
        self.load()

    def add(self, new_score: Score):
        new_score.date_added = datetime.now()
        self.__scores.append(new_score)

    def get(self):
        return sorted(self.__scores, key=lambda x: x.score, reverse=True)

    def load(self):
        try:
            with open(self.__highscores_filename, 'rb') as file:
                self.__scores = pickle.load(file)
                logging.info(f'Highscores loaded from "{self.__highscores_filename}".')
        except FileNotFoundError:
            logging.info(f'File "{self.__highscores_filename}" not found.')

    def save(self):
        # noinspection PyBroadException
        try:
            with open(self.__highscores_filename, 'wb') as file:
                pickle.dump(self.__scores, file)
                logging.info(f'Highscores saved to "{self.__highscores_filename}".')
        except:
            logging.info(f'An error has occured while trying to save to "{self.__highscores_filename}".')


if __name__ == '__main__':
    hs = Highscores()
    for i, score in enumerate(hs.get()):
        print(f'{i + 1}. {score}')
