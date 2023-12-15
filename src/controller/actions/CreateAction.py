from src.controller.actions.Action import Action, Output, request
from src.model.feed.facade.FeedFacade import FeedFacade, FeedDTO

class CreateAction(Action):

    def exec(self, request : request) -> Output:
        output = Output()
        try:
            feed : FeedDTO = FeedDTO(**request.form)
            _ = FeedFacade().create_feed(feed)
            output.status = 1
        except Exception as e:
            output.error : Exception = e
            output.status = -1
        return output