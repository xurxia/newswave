import importlib
from src.model.common.Config import Config
from src.model.feed.dao.FeedDAOInterface import FeedDAOInterface

class FeedDAOFactory():

    def __new__(cls):
        if not hasattr(cls, '_singleton'):
            cls._singleton = super(FeedDAOFactory, cls).__new__(cls)
        return cls._singleton

    def get_feed_dao(self):
        if not hasattr(self, '_instance'):
            config = Config()
            section = config.get_str('DATABASE', 'TYPE')
            driver = config.get_str(section, 'DRIVER')
            module_name : str = f'src.model.feed.dao.Feed{driver}DAO'
            class_name : str =  f'Feed{driver}DAO'
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
            self._instance = class_()
        return self._instance
    