import feedparser
from datetime import datetime
from time import mktime

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
    
    def get_feed(self, id : int) -> [FeedDTO | None]:
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
            parsed : dict = feedparser.parse(feed.url)
            for entry in parsed['entries']:
                title : str =((entry['title']).encode(encoding=parsed['encoding'], errors="ignore")).decode("utf-8")
                link : str = ((entry['link']).encode(encoding=parsed['encoding'], errors="ignore")).decode("utf-8")
                published : datetime = datetime.fromtimestamp(mktime(entry['published_parsed']))
                entries.append(EntryDTO(title, link, published))
        except Exception as e:
            raise ModelException(f'Error getting entries from {feed.name} feed: '+e.message)
        return entries