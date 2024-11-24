from configparser import ConfigParser, NoSectionError, NoOptionError

from src.model.exception.ModelException import ModelException

DEFAULT_FILE = './src/config/configdev.ini'

class Config():

    def __new__(cls, file = DEFAULT_FILE):
        if not hasattr(cls, '_singleton'):
            cls._singleton = super(Config, cls).__new__(cls)
        return cls._singleton
    
    def __init__(self, file =DEFAULT_FILE):
        if not hasattr(self, '_config'):
            self._config =  ConfigParser()
            try:
                self._config.read(file)
            except Exception as e:
                raise ModelException(f'Error reading config file: {file}')
    
    def _get(self, section : str, parameter : str) -> str | int | float | None:
        try:
            return self._config.get(section, parameter)
        except NoSectionError as e:
            raise ModelException(f'Error setting section {section}')
        except NoOptionError as e:
            raise ModelException(f'Error setting parameter {parameter} in section {section}')
        except Exception as e:
            raise ModelException('Error setting a parameter in config file')

    def _set(self, section: str, parameter : str, value : float) -> None:
        try:
            self._config.set(section, parameter, value)
        except NoSectionError as e:
            raise ModelException(f'Error getting section {section}')
        except NoOptionError as e:
            raise ModelException(f'Error getting parameter {parameter} from section {section}')
        except Exception as e:
            raise ModelException('Error accesing a parameter from config file')


    def get_str(self, section : str, parameter : str) -> str | None:
        try:
            return self._get(section, parameter)
        except Exception as e:
            raise e
        
    def set_str(self, section: str, parameter : str, value : str) -> None:
        try:
            return self._set(section, parameter, value)
        except Exception as e:
            raise e
        
    def get_int(self, section : str, parameter : str) -> int | None:
        try:
            return self._get(section, parameter)
        except Exception as e:
            raise e
            
    def set_int(self, section: str, parameter : str, value : int) -> None:
        try:
            return self._set(section, parameter, value)
        except Exception as e:
            raise e
        
    def get_float(self, section : str, parameter : str) -> float | None:
        try:
            return self._get(section, parameter)
        except Exception as e:
            raise e
        
    def set_flotat(self, section: str, parameter : str, value : float) -> None:
        try:
            return self._set(section, parameter, value)
        except Exception as e:
            raise e
        
    def write(self, file = DEFAULT_FILE) -> None:
        try:
            with open(file, 'w') as fp:
                self._config.write(fp)
        except Exception as e:
            raise ModelException(f'Error writing config file: {file}')
