from src.model.feed.dto.FeedDTO import FeedDTO

class FeedDAOInterface():

    def create_feed(self, feed : FeedDTO) -> int:
        pass

    def get_feed(self, id : int) -> FeedDTO:
        pass

    def get_feeds(self) -> list[FeedDTO]:
        pass
    
    def update_feed(self, feed : FeedDTO) -> None:
        pass

    def delete_feed(self, id : int) -> None:
        pass