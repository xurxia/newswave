import sqlite3
from typing import TypeAlias

from src.model.common.Config import Config
from src.model.feed.dao.FeedDAOInterface import FeedDAOInterface, FeedDTO
from src.model.exception.ModelException import ModelException

Connection : TypeAlias = sqlite3.Connection
Cursor : TypeAlias = sqlite3.Cursor
Row : TypeAlias = sqlite3.Row

class FeedSQLiteDAO(FeedDAOInterface):

    def __init__(self):
        try:
            config : Config = Config()
            driver : str = config.get_str('DATABASE', 'TYPE')
            db_name : str  = config.get_str(driver, 'PATH')        
            self._connection : Connection = sqlite3.connect(db_name, check_same_thread = False)
        except ModelException as e:
            raise ModelException(f'Error reading FeedSQLiteDAO config: '+e.message)
        except sqlite3.Error:
            raise ModelException(f'Error connecting to SQLite3 Database')
        
    def _execute_sql(self, sql :str, params : dict = {}) -> sqlite3.Cursor:
        try:
            cursor : Cursor = self._connection.cursor()
            cursor.execute(sql, params)
        except sqlite3.Error as e:
            raise ModelException(f'Error executing SQLite3 query: {sql}')
        return cursor
    
    def _commit(self):
        try:
            self._connection.commit()
        except sqlite3.Error as e:
            raise ModelException(f'Error commiting SQLite3')
        
    def create_feed(self, feed : FeedDTO) -> int:
        try:
            sql : str = f'INSERT INTO SOURCE (NAME, URL) VALUES (:name, :url)'
            params : dict = {'name': feed.name, 'url': feed.url}
            cursor = self._execute_sql(sql, params)
            if cursor.rowcount == 1:
                self._commit()
                id = cursor.lastrowid
            else:
                raise ModelException(f'rowcount <> 1')
        except ModelException as e:
            raise ModelException(f'Error creating feed at SQLite3 database: '+e.message)
        except Exception as e:
            raise ModelException(f'Unknow error creating feed at SQLite3 database')
        return id
           
    def get_feed(self, id : int) -> FeedDTO:
        try:
            sql : str = f'SELECT ID, NAME, URL FROM SOURCE WHERE ID=:id'
            params : dict = {'id': id}
            cursor : Cursor = self._execute_sql(sql, params)
            row : Row = cursor.fetchone()
            feed : FeedDTO = None
            if row is not None:
                feed = FeedDTO(row[0], row[1], row[2])
        except ModelException as e:
            raise ModelException(f'Error getting feed at SQLite3 database: '+e.message)
        except Exception as e:
            raise ModelException(f'Unknow error getting feed at SQLite3 database')
        return feed
    
    def get_feeds(self) -> list[FeedDTO]:
        try:
            sql : str = f'SELECT ID, NAME, URL FROM SOURCE'
            cursor : Cursor = self._execute_sql(sql)
            rows : list[Row] = cursor.fetchall()
            feeds : list[FeedDTO] = []
            for row in rows:
                feed : FeedDTO = FeedDTO(row[0], row[1], row[2])
                feeds.append(feed)
        except ModelException as e:
            raise ModelException(f'Error getting feeds at SQLite3 database: '+e.message)
        except Exception as e:
            raise ModelException(f'Unknow error getting feeds at SQLite3 database')
        return feeds
       
    def update_feed(self, feed : FeedDTO) -> None:
        try:
            sql : str = f'UPDATE SOURCE SET NAME=:name, URL=:url WHERE ID=:id'
            params : dict = {'id': feed.id, 'name': feed.name, 'url': feed.url}
            cursor : Cursor = self._execute_sql(sql, params)
            if cursor.rowcount == 1:
                self._commit()
            else:
                raise ModelException(f'rowcount <> 1')
        except ModelException as e:
            raise ModelException(f'Error updating feed at SQLite3 database: '+e.message)
        except Exception as e:
            raise ModelException(f'Unknow error updating feed at SQLite3 database')

    def delete_feed(self, id : int) -> None:
        try:
            sql : str = f'DELETE FROM SOURCE WHERE ID=:id'
            params : dict = {'id': id}
            cursor : Cursor = self._execute_sql(sql, params)
            if cursor.rowcount == 1:
                self._commit()
            else:
                raise ModelException(f'rowcount <> 1')
        except ModelException as e:
            raise ModelException(f'Error deleting feed at SQLite3 database: '+e.message)
        except Exception as e:
            raise ModelException(f'Unknow error deleting feed at SQLite3 database')