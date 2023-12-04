from time import mktime
from datetime import datetime, timedelta
import sqlite3
import feedparser

from src.model.common.Config import Config

class Parser():
	
    def __init__(self):
        config = Config()
        self._file = config.get_str('GENERAL', 'FILE')
        self._db_name = config.get_str('SQLITE3', 'PATH')

    def _get_feeds(self) -> dict:
        con = sqlite3.connect(self._db_name)
        sources = con.execute("SELECT NAME, URL FROM SOURCE")
        return sources
    
    def process(self) -> None:
        sources = self._get_feeds()

        date_min = datetime.now() + timedelta(days=-2)
        html = '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body>'
        for source in sources:
            html += f'<H2>Fuente: {source[0]}</H2>'
            html += "<ul>"
            feeds = feedparser.parse(source[1])
            for feed in feeds['entries']:
                timestamp = feed['published_parsed']
                date = datetime.fromtimestamp(mktime(timestamp))
                if date > date_min:
                    title = ((feed['title']).encode(encoding=feeds['encoding'], errors="ignore")).decode("utf-8")
                    link = ((feed['link']).encode(encoding=feeds['encoding'], errors="ignore")).decode("utf-8")
                    html += f'<li>{str(date)} : <a href="{link}">{title}</a></li>'
            html += '</ul>'
        html += "</body></html>"

        output = open(self._file, "w", encoding="utf-8")
        output.write(html)
        output.close()