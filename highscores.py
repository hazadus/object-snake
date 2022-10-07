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
    highscores_filename = 'highscores.pkl'
    scores = list()

    def __init__(self):
        self.load()

    def add(self, new_score: Score):
        new_score.date_added = datetime.now()
        self.scores.append(new_score)

    def get(self):
        return sorted(self.scores, key=lambda x: x.score, reverse=True)

    def load(self):
        try:
            with open(self.highscores_filename, 'rb') as file:
                self.scores = pickle.load(file)
                logging.info(f'Highscores loaded from "{self.highscores_filename}".')
                for i, score in enumerate(self.get()):
                    logging.info(f'{i + 1}. {score}')
        except FileNotFoundError:
            logging.info(f'File "{self.highscores_filename}" not found.')

    def save(self):
        # noinspection PyBroadException
        try:
            with open(self.highscores_filename, 'wb') as file:
                pickle.dump(self.scores, file)
                logging.info(f'Highscores saved to "{self.highscores_filename}".')
        except:
            logging.info(f'An error has occured while trying to save to "{self.highscores_filename}".')
