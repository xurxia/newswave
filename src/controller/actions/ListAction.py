from src.controller.actions.Action import Action, Output, Request
from src.model.feed.facade.FeedFacade import FeedFacade, FeedDTO

class ListAction(Action):

    def exec(self, request : Request) -> Output:
        output = Output()
        try:
            output.vars["feeds"] : list[FeedDTO] = FeedFacade().get_feeds()
            output.status = 1
        except Exception as e:
            output.error : Exception = e
            output.status = -1
        return output