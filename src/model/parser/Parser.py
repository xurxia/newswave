from time import mktime
from datetime import datetime, timedelta

from src.model.common.Config import Config
from src.model.feed.facade.FeedFacade import FeedFacade, FeedDTO, EntryDTO

class Parser():
	
    def __init__(self):
        config : Config = Config()
        self._file : str = config.get_str('GENERAL', 'FILE')

    def _get_feeds(self) -> dict:
        facade : FeedFacade = FeedFacade()
        sources : list[FeedDTO] = facade.get_feeds()
        return sources
    
    def process(self) -> None:
        date_min : datetime = datetime.now() + timedelta(days=-2)
        html = '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body>'
        sources : list[FeedDTO] = self._get_feeds()
        for source in sources:
            html += f'<H2>Fuente: {source.name}</H2>'
            html += "<ul>"
            entries = FeedFacade().get_entries(source)
            for entry in entries:
                if entry.published > date_min:
                    html += f'<li>{str(entry.published)} : <a href="{entry.link}">{entry.title}</a></li>'
            html += '</ul>'
        html += "</body></html>"

        output = open(self._file, "w", encoding="utf-8")
        output.write(html)
        output.close()