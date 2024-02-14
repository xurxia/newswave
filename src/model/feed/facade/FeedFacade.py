import feedparser
from datetime import datetime
from time import mktime
from typing import Union

from src.model.feed.dao.FeedDAOFactory import FeedDAOFactory
from src.model.feed.dao.FeedDAOInterface import FeedDAOInterface
from src.model.feed.dto.FeedDTO import FeedDTO
from src.model.entry.dto.EntryDTO import EntryDTO
from src.model.exception.ModelException import ModelException

class FeedFacade():

    def create_feed(self, feed : FeedDTO) -> int:
        try:
            dao : FeedDAOInterface = FeedDAOFactory().get_feed_dao()
            id : int = dao.create_feed(feed)
        except ModelException as e:
            raise ModelException(f'Error creating feed: '+e.message)
        return id
    
    def get_feed(self, id : int) -> Union[FeedDTO | None]:
        try:
            dao : FeedDAOInterface = FeedDAOFactory().get_feed_dao()
            feed : FeedDTO = dao.get_feed(id)
        except ModelException as e:
            raise ModelException(f'Error getting feed: '+e.message)
        return feed
    
    def get_feeds(self) -> list[FeedDTO]:
        try:
            dao : FeedDAOInterface = FeedDAOFactory().get_feed_dao()
            feeds : list[FeedDTO] = dao.get_feeds()
        except ModelException as e:
            raise ModelException(f'Error getting feeds: '+e.message)
        return feeds
    
    def update_feed(self, feed : FeedDTO) -> None:
        try:
            dao : FeedDAOInterface = FeedDAOFactory().get_feed_dao()
            dao.update_feed(feed)
        except ModelException as e:
            raise ModelException(f'Error updating feed: '+e.message)
    
    def delete_feed(self, id : int) -> None:
        try:
            dao : FeedDAOInterface = FeedDAOFactory().get_feed_dao()
            dao.delete_feed(id)
        except ModelException as e:
            raise ModelException(f'Error deleting feed: '+e.message)
    
    def get_entries(self, feed : FeedDTO) -> list[EntryDTO]:
        try:
            entries : list[EntryDTO] = []
            parsed : dict = feedparser.parse(feed.url, etag=feed.etag)
            if((etag := parsed.get('etag')) is not None):
                feed.etag = etag
                self.update_feed(feed)
            for entry in parsed['entries']:
                author : str
                summary : str
                tags : list[str] = []
                title : str =((entry['title']).encode(encoding=parsed['encoding'], errors="ignore")).decode("utf-8")
                link : str = ((entry['link']).encode(encoding=parsed['encoding'], errors="ignore")).decode("utf-8")
                published : datetime = datetime.fromtimestamp(mktime(entry['published_parsed']))
                if ((author := entry.get('author')) is not None):
                    author = (author.encode(encoding=parsed['encoding'], errors="ignore")).decode("utf-8")
                if ((summary := entry.get('summary')) is not None):
                    summary = (summary.encode(encoding=parsed['encoding'], errors="ignore")).decode("utf-8")
                if ((tags_tmp := entry.get('tags')) is not None):
                    for tag in tags_tmp:
                        if(tag.term is not None):
                            tags.append(tag.term)
                entries.append(EntryDTO(title, link, published, author, summary, tags))
        except Exception as e:
            raise ModelException(f'Error getting entries from {feed.name} feed: {e}')
        return entries