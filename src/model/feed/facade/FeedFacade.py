import feedparser
from datetime import datetime, timedelta
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
    
    def _process_entry(self, entry : EntryDTO, encoding : str, start_date : datetime) -> Union[EntryDTO, None]:
        published : datetime
        author : str
        summary : str
        tags : list[str] = []
        title : str =((entry['title']).encode(encoding=encoding, errors="ignore")).decode("utf-8")
        link : str = ((entry['link']).encode(encoding=encoding, errors="ignore")).decode("utf-8")
        if ((published := entry.get('published_parsed')) is not None):
            published = datetime.fromtimestamp(mktime(published))
        elif ((published := entry.get('updated_parsed')) is not None):
            published = datetime.fromtimestamp(mktime(published))
        else:
            published = 0
        if ((author := entry.get('author')) is not None):
            author = (author.encode(encoding=encoding, errors="ignore")).decode("utf-8")
        if ((summary := entry.get('summary')) is not None):
            summary = (summary.encode(encoding=encoding, errors="ignore")).decode("utf-8")
        if ((tags_tmp := entry.get('tags')) is not None):
            for tag in tags_tmp:
                if(tag.term is not None):
                    tags.append(tag.term)
        if published > start_date:
            return EntryDTO(title, link, published, author, summary, tags)
        else:
            return None

    def _get_start_date(self, feed : FeedDTO, days : int) -> datetime:
        if(feed.updated != ''):
            start_date : datetime = datetime.strptime(feed.updated, '%Y-%m-%d %H:%M:%S')
        else:
            start_date : datetime = datetime.now() - timedelta(days=days)
        return start_date

    def _get_updated(self, parsed : dict) -> str:
        updated : str = ''
        if((updated := parsed.feed.get('updated_parsed')) is not None):
            updated = str(datetime(*updated[:6]))
        elif len(parsed.get('entries', [])) > 0:
            updated = str(datetime(*parsed.entries[0].published_parsed[:6]))
        return updated
    
    def get_entries(self, feed : FeedDTO, days : int = 2) -> list[EntryDTO]:
        try:
            entries : list[EntryDTO] = []
            parsed : dict = feedparser.parse(feed.url, etag=feed.etag, modified=feed.modified)
            start_date : datetime = self._get_start_date(feed, days)
            feed.etag = parsed.get('etag', '')
            feed.modified = parsed.get('modified', '')
            if((updated := self._get_updated(parsed)) != ''):
                feed.updated = updated
            self.update_feed(feed)
            for entry in parsed['entries']:
                encoding : str = parsed['encoding']
                if((processed := self._process_entry(entry, encoding, start_date)) != None):
                    entries.append(processed)
        except Exception as e:
            raise ModelException(f'Error getting entries from {feed.name} feed: {e}')
        return entries