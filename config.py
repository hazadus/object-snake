import tomli
import logging


class Config:
    def __init__(self, full_file_path: str):
        self.config_dict = None
        try:
            with open(full_file_path, "rb") as file:
                self.config_dict = tomli.load(file)
                logging.info(f'Config loaded from "{full_file_path}".')
        except FileNotFoundError:
            logging.info(f'Can\'t load config from "{full_file_path}", using defaults.')
        except tomli.TOMLDecodeError:
            logging.info(f'Wrong file format - "{full_file_path}"! Using defaults.')
        finally:
            if self.config_dict is None:
                self.config_dict = dict()
            # Check config and set to defaults if parameters are missing
            if not self.config_dict.get('board_width'):
                self.config_dict['board_width'] = 40
            if not self.config_dict.get('board_height'):
                self.config_dict['board_height'] = 40
            if not self.config_dict.get('block_size'):
                self.config_dict['block_size'] = 17
            if not self.config_dict.get('player_name'):
                self.config_dict['player_name'] = 'hazadus'

    def __getitem__(self, item):
        return self.config_dict.get(item)
