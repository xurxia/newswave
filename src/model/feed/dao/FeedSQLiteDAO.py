import sqlite3

from src.model.common.Config import Config
from src.model.feed.dao.FeedDAOInterface import FeedDAOInterface, FeedDTO

class FeedSQLiteDAO(FeedDAOInterface):

    def __init__(self):
        config = Config()
        driver = config.get_str('DATABASE', 'TYPE')
        db_name = config.get_str(driver, 'PATH')
        self._connection = sqlite3.connect(db_name)

    def _execute_sql(self, sql :str, params : dict = {}) -> sqlite3.Cursor:
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        return cursor
    
    def _commit(self):
        self._connection.commit()

    def create_feed(self, feed : FeedDTO) -> int:
        sql = f'INSERT INTO SOURCE (NAME, URL) VALUES (:name, :url)'
        params = {'name': feed.name, 'url': feed.url}
        cursor = self._execute_sql(sql, params)
        if cursor.rowcount == 1:
            self._commit()
            id = cursor.lastrowid
        else:
            id = -1
        return id
           
    def get_feed(self, id : int) -> FeedDTO:
        sql = f'SELECT ID, NAME, URL FROM SOURCE WHERE ID=:id'
        params = {'id': id}
        cursor = self._execute_sql(sql, params)
        row = cursor.fetchone()
        if row is not None:
            feed = FeedDTO(row[0], row[1], row[2])
        else:
            feed = None
        return feed
    
    def get_feeds(self) -> list[FeedDTO]:
        sql = f'SELECT ID, NAME, URL FROM SOURCE'
        cursor = self._execute_sql(sql)
        rows = cursor.fetchall()
        feeds = []
        for row in rows:
            feed = FeedDTO(row[0], row[1], row[2])
            feeds.append(feed)
        return feeds
       
    def update_feed(self, feed : FeedDTO) -> int:
        sql = f'UPDATE SOURCE SET NAME=:name, URL=:url WHERE ID=:id'
        params = {'id': feed.id, 'name': feed.name, 'url': feed.url}
        cursor = self._execute_sql(sql, params)
        if cursor.rowcount == 1:
            self._commit()
            updated = 1
        else:
            updated = -1
        return updated

    def delete_feed(self, id : int) -> int:
        sql = f'DELETE FROM SOURCE WHERE ID=:id'
        params = {'id': id}
        cursor = self._execute_sql(sql, params)
        if cursor.rowcount == 1:
            self._commit()
            deleted = 1
        else:
            deleted = -1
        return deleted