import sqlite3
from typing import TypeAlias

from src.model.common.Config import Config
from src.model.feed.dao.FeedDAOInterface import FeedDAOInterface, FeedDTO

Connection : TypeAlias = sqlite3.Connection
Cursor : TypeAlias = sqlite3.Cursor
Row : TypeAlias = sqlite3.Row

class FeedSQLiteDAO(FeedDAOInterface):

    def __init__(self):
        config : Config = Config()
        driver : str = config.get_str('DATABASE', 'TYPE')
        db_name : str  = config.get_str(driver, 'PATH')
        self._connection : Connection = sqlite3.connect(db_name)

    def _execute_sql(self, sql :str, params : dict = {}) -> sqlite3.Cursor:
        cursor : Cursor = self._connection.cursor()
        cursor.execute(sql, params)
        return cursor
    
    def _commit(self):
        self._connection.commit()

    def create_feed(self, feed : FeedDTO) -> int:
        sql : str = f'INSERT INTO SOURCE (NAME, URL) VALUES (:name, :url)'
        params : dict = {'name': feed.name, 'url': feed.url}
        cursor = self._execute_sql(sql, params)
        id : int = -1
        if cursor.rowcount == 1:
            self._commit()
            id = cursor.lastrowid
        return id
           
    def get_feed(self, id : int) -> FeedDTO:
        sql : str = f'SELECT ID, NAME, URL FROM SOURCE WHERE ID=:id'
        params : dict = {'id': id}
        cursor : Cursor = self._execute_sql(sql, params)
        row : Row = cursor.fetchone()
        feed : FeedDTO = None
        if row is not None:
            feed = FeedDTO(row[0], row[1], row[2])
        return feed
    
    def get_feeds(self) -> list[FeedDTO]:
        sql : str = f'SELECT ID, NAME, URL FROM SOURCE'
        cursor : Cursor = self._execute_sql(sql)
        rows : list[Row] = cursor.fetchall()
        feeds : list[FeedDTO] = []
        for row in rows:
            feed : FeedDTO = FeedDTO(row[0], row[1], row[2])
            feeds.append(feed)
        return feeds
       
    def update_feed(self, feed : FeedDTO) -> int:
        sql : str = f'UPDATE SOURCE SET NAME=:name, URL=:url WHERE ID=:id'
        params : dict = {'id': feed.id, 'name': feed.name, 'url': feed.url}
        cursor : Cursor = self._execute_sql(sql, params)
        updated : int = -1
        if cursor.rowcount == 1:
            self._commit()
            updated = 1
        return updated

    def delete_feed(self, id : int) -> int:
        sql : str = f'DELETE FROM SOURCE WHERE ID=:id'
        params : dict = {'id': id}
        cursor : Cursor = self._execute_sql(sql, params)
        deleted : int = -1
        if cursor.rowcount == 1:
            self._commit()
            deleted = 1
        return deleted