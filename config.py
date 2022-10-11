import tomli
import logging


class Config:
    """
    Загружает конфигурацию из файла в формате TOML.

    __defaults: словарь с настройками по умолчанию, используется при отсутствии файла конфигурации или отдельных
                параметров в нём.

    Args
        full_file_path (str): полный путь к файлу конфигурации в формате TOML.
    """
    __defaults = {
        'log_filename': 'object-snake.log',
        'board_width': 40,
        'board_height': 40,
        'block_size': 17,
        'player_name': 'hazadus',
        'window_caption': 'Objective Snake',
        'margin_top': 25,
        'base_speed': 5,
        'font_logo_name': 'PT Mono',
        'font_info_line_name': 'PT Mono',
        'font_paused_name': 'Chalkboard'
    }

    def __init__(self, full_file_path: str):
        self.__config_dict = None

        try:
            with open(full_file_path, "rb") as file:
                self.__config_dict = tomli.load(file)
                logging.info(f'Config loaded from "{full_file_path}".')
        except FileNotFoundError:
            logging.info(f'Can\'t load config from "{full_file_path}", using defaults.')
        except tomli.TOMLDecodeError:
            logging.info(f'Wrong file format - "{full_file_path}"! Using defaults.')
        finally:
            if self.__config_dict is None:
                self.__config_dict = dict()

            for key in self.__defaults:
                if not self.__config_dict.get(key):
                    self.__config_dict[key] = self.__defaults[key]
                    logging.info(f'Key "{key}" missing in config "{full_file_path}", '
                                 f'using default {key}="{self.__defaults[key]}"')

    def __getitem__(self, key):
        """
        Возвращает параметр конфигурации с использованием скобок [] с именем инстанса класса.
        :param key: Ключ (параметр) настроек
        :return: Значение параметра по указанному ключу
        """
        return self.__config_dict.get(key)
