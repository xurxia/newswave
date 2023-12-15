from configparser import ConfigParser, NoSectionError, NoOptionError

from src.model.exception.ModelException import ModelException

class Config():

    def __new__(cls, file = './src/config/config.ini'):
        if not hasattr(cls, '_singleton'):
            cls._singleton = super(Config, cls).__new__(cls)
        return cls._singleton
    
    def __init__(self, file = './src/config/config.ini'):
        if not hasattr(self, '_config'):
            self._config =  ConfigParser()
            try:
                self._config.read(file)
            except Exception as e:
                raise ModelException(f'Error reading config file: {file}')
    
    def get_str(self, section : str, parameter : str) -> str | None:
        try:
            return self._config.get(section, parameter)
        except NoSectionError as e:
            raise ModelException(f'Error getting section {section}')
        except NoOptionError as e:
            raise ModelException(f'Error getting parameter {parameter} from section {section}')
        except Exception as e:
            raise ModelException('Error accesing a parameter from config file')
    
    def get_int(self, section : str, parameter : str) -> int | None:
        try:
            return self._config.getint(section, parameter)
        except NoSectionError as e:
            raise ModelException(f'Error getting section {section}')
        except NoOptionError as e:
            raise ModelException(f'Error getting parameter {parameter} from section {section}')
        except Exception as e:
            raise ModelException('Error accesing a parameter from config file')
    
    def get_float(self, section : str, parameter : str) -> float | None:
        try:
            return self._config.getfloat(section, parameter)
        except NoSectionError as e:
            raise ModelException(f'Error getting section {section}')
        except NoOptionError as e:
            raise ModelException(f'Error getting parameter {parameter} from section {section}')
        except Exception as e:
            raise ModelException('Error accesing a parameter from config file')