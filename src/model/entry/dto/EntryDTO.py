from datetime import datetime

class EntryDTO():

    def __init__(self, title : str, link : str, published : datetime):
        self._title : str = title
        self._link : str = link
        self._published : datetime = published

    def _get_title(self) -> str:
        return self._title

    title = property(_get_title, None, None)

    def _get_link(self) -> str:
        return self._link

    link = property(_get_link, None, None)

    def _get_published(self) -> datetime:
        return self._published
    
    published = property(_get_published, None, None)