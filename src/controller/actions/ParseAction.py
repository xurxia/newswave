from src.controller.actions.Action import Action, Output, Request
from src.model.feed.facade.FeedFacade import FeedFacade, FeedDTO

class ParseAction(Action):

    def __init__(self):
        self._feed_facade : FeedFacade = FeedFacade()

    def exec(self, request : Request) -> Output:
        output = Output()
        try:
            feeds: list[FeedDTO] = self._feed_facade.get_feeds()
            for feed in feeds:
                entries = self._feed_facade.get_entries(feed, days=2)
                feed.__dict__['entries'] = entries
            output.vars["feeds"] = feeds
            output.status = 1
        except Exception as e:
            output.error : Exception = e
            output.status = -1
        print(output.status)
        return output