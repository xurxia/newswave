from src.model.common.Config import Config
from src.model.feed.facade.FeedFacade import FeedFacade, FeedDTO, EntryDTO, ModelException

class Parser():
	
    def __init__(self):
        config : Config = Config()
        self._file : str = config.get_str('GENERAL', 'FILE')
        self._feed_facade : FeedFacade = FeedFacade()

    def process(self, days : int = 2) -> None:
        html = '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body>'
        feeds : list[FeedDTO] = self._feed_facade.get_feeds()
        for feed in feeds:
            html_tmp = ''
            try:
                print(f'Source: {feed.name}')
                html_tmp += f'<H2>Fuente: {feed.name}</H2>'
                html_tmp += "<ul>"
                entries = self._feed_facade.get_entries(feed, days)
                for entry in entries:
                    html_tmp += f'<li>{str(entry.published)} by [{entry.author}]'
                    for tag in entry.tags:
                        html_tmp += f' #{tag}'
                    html_tmp += f': <a href="{entry.link}">{entry.title}</a></li>'
                html_tmp += '</ul>'
            except ModelException as e:
                print(f'Error parsing feed {feed.name}: {e}' )
            else:
                html += html_tmp
        html += "</body></html>"
        with open(self._file, "w", encoding="utf-8") as output:
            output.write(html)
            output.close()