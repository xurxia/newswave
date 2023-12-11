import feedparser
from datetime import datetime
from time import mktime

from src.model.feed.dao.FeedDAOFactory import FeedDAOFactory
from src.model.feed.dao.FeedDAOInterface import FeedDAOInterface
from src.model.feed.dto.FeedDTO import FeedDTO
from src.model.entry.dto.EntryDTO import EntryDTO

class FeedFacade():

    def create_feed(self, feed : FeedDTO) -> int:
        dao : FeedDAOInterface = FeedDAOFactory().get_feed_dao()
        id : int = dao.create_feed(feed)
        return id
    
    def get_feed(self, id : int) -> [FeedDTO | None]:
        dao : FeedDAOInterface = FeedDAOFactory().get_feed_dao()
        feed : FeedDTO = dao.get_feed(id)
        return feed
    
    def get_feeds(self) -> list[FeedDTO]:
        dao : FeedDAOInterface = FeedDAOFactory().get_feed_dao()
        feeds : list[FeedDTO] = dao.get_feeds()
        return feeds
    
    def update_feed(self, feed : FeedDTO) -> bool:
        dao : FeedDAOInterface = FeedDAOFactory().get_feed_dao()
        result : int = dao.update_feed(feed)
        return result==1
    
    def delete_feed(self, id : int) -> bool:
        dao : FeedDAOInterface = FeedDAOFactory().get_feed_dao()
        result : int = dao.delete_feed(id)
        return result==1
    
    def get_entries(self, feed : FeedDTO) -> list[EntryDTO]:
        entries : list[EntryDTO] = []
        parsed : dict = feedparser.parse(feed.url)
        for entry in parsed['entries']:
            title : str =((entry['title']).encode(encoding=parsed['encoding'], errors="ignore")).decode("utf-8")
            link : str = ((entry['link']).encode(encoding=parsed['encoding'], errors="ignore")).decode("utf-8")
            published : datetime = datetime.fromtimestamp(mktime(entry['published_parsed']))
            entries.append(EntryDTO(title, link, published))
        return entries