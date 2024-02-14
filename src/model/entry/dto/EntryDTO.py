from datetime import datetime

class EntryDTO():

    def __init__(self, title : str, link : str, published : datetime, author : str, summary : str, tags : list[str]):
        self._title : str = title
        self._link : str = link
        self._published : datetime = published
        self._author : str = author
        self._summary : str = summary
        self._tags : list[str] = tags

    def _get_title(self) -> str:
        return self._title

    title = property(_get_title, None, None)

    def _get_link(self) -> str:
        return self._link

    link = property(_get_link, None, None)

    def _get_published(self) -> datetime:
        return self._published
    
    published = property(_get_published, None, None)

    def _get_author(self) -> str:
        return self._author
    
    author = property(_get_author, None, None)

    def _get_summary(self) -> str:
        return self._summary
    
    summary = property(_get_summary, None, None)

    def _get_tags(self) -> list[str]:
        return self._tags
    
    tags = property(_get_tags, None, None)