from src.controller.actions.Action import Action, Output, Request
from src.model.feed.facade.FeedFacade import FeedFacade, FeedDTO

class UpdateAction(Action):

    def exec(self, request : Request) -> Output:
        output = Output()
        try:
            feed : FeedDTO = FeedDTO(**request.form)
            _ = FeedFacade().update_feed(feed)
            output.status = 1
        except Exception as e:
            output.error : Exception = e
            output.status = -1
        return output