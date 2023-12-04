from configparser import ConfigParser

class Config():

    def __new__(cls, file = './src/config/config.ini'):
        if not hasattr(cls, '_singleton'):
            cls._singleton = super(Config, cls).__new__(cls)
        return cls._singleton
    
    def __init__(self, file = './src/config/config.ini'):
        if not hasattr(self, '_config'):
            self._config =  ConfigParser()
            self._config.read(file)
    
    def get_str(self, section : str, parameter : str) -> str | None:
        return self._config.get(section, parameter)
    
    def get_int(self, section : str, parameter : str) -> int | None:
        return self._config.getint(section, parameter)
    
    def get_float(self, section : str, parameter : str) -> float | None:
        return self._config.getfloat(section, parameter)
    