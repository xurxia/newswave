from jinja2 import Environment, FileSystemLoader
from src.model.common.Config import Config
from src.model.feed.facade.FeedFacade import FeedFacade, FeedDTO, EntryDTO, ModelException

class Parser():
	
    def __init__(self):
        config : Config = Config()
        self._file : str = config.get_str('GENERAL', 'FILE')
        self._feed_facade : FeedFacade = FeedFacade()

    def process(self, days : int = 2) -> str:
        env = Environment(loader=FileSystemLoader('./src/view'))
        template = env.get_template('parser/resume.html')
        feeds : list[FeedDTO] = self._feed_facade.get_feeds()
        for feed in feeds:
            try:
                entries = self._feed_facade.get_entries(feed, days)
                feed.__dict__['entries']=entries
            except ModelException as e:
                print(f'Error parsing feed {feed.name}: {e}' )
        html : str = template.render(feeds=feeds)
        return html