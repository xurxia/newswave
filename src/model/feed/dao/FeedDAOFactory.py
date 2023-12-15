import importlib
from types import ModuleType

from src.model.common.Config import Config
from src.model.exception.ModelException import ModelException

class FeedDAOFactory():

    def __new__(cls):
        if not hasattr(cls, '_singleton'):
            cls._singleton = super(FeedDAOFactory, cls).__new__(cls)
        return cls._singleton

    def get_feed_dao(self):
        if not hasattr(self, '_instance'):
            try:
                config : Config = Config()
                section : str = config.get_str('DATABASE', 'TYPE')
                driver : str = config.get_str(section, 'DRIVER')
                module_name : str = f'src.model.feed.dao.Feed{driver}DAO'
                class_name : str =  f'Feed{driver}DAO'
            except ModelException as e:
                raise ModelException(f'Error reading FeedDAOFactory config: '+e.message)
            
            try:
                module : ModuleType  = importlib.import_module(module_name)
                class_ = getattr(module, class_name)
                self._instance = class_()
            except Exception as e:
                raise ModelException(f'Error instantiating an {class_name} object \
                                     from {module_name} module')
            
        return self._instance