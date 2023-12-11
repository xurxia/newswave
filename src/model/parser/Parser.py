from time import mktime
from datetime import datetime, timedelta

from src.model.common.Config import Config
from src.model.feed.facade.FeedFacade import FeedFacade, FeedDTO, EntryDTO

class Parser():
	
    def __init__(self):
        config : Config = Config()
        self._file : str = config.get_str('GENERAL', 'FILE')
        self._feed_facade : FeedFacade = FeedFacade()

    def process(self, days : int = 2) -> None:
        start_date : datetime = datetime.now() + timedelta(days=days)
        html = '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body>'
        feeds : list[FeedDTO] = self._feed_facade.get_feeds()
        for feed in feeds:
            html += f'<H2>Fuente: {feed.name}</H2>'
            html += "<ul>"
            entries = self._feed_facade.get_entries(feed)
            for entry in entries:
                if entry.published > start_date:
                    html += f'<li>{str(entry.published)} : <a href="{entry.link}">{entry.title}</a></li>'
            html += '</ul>'
        html += "</body></html>"
        with open(self._file, "w", encoding="utf-8") as output:
            output.write(html)
            output.close()