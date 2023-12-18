from abc import ABC, abstractmethod

from src.model.feed.dto.FeedDTO import FeedDTO

class FeedDAOInterface(ABC):

    @abstractmethod
    def create_feed(self, feed : FeedDTO) -> int:
        pass

    @abstractmethod
    def get_feed(self, id : int) -> FeedDTO:
        pass

    @abstractmethod
    def get_feeds(self) -> list[FeedDTO]:
        pass
    
    @abstractmethod
    def update_feed(self, feed : FeedDTO) -> None:
        pass

    @abstractmethod
    def delete_feed(self, id : int) -> None:
        pass