from src.controller.actions.Action import Action, Output, Request
from src.model.feed.facade.FeedFacade import FeedFacade, FeedDTO

class DeleteAction(Action):

    def exec(self, request : Request) -> Output:
        output = Output()
        try:
            _ = FeedFacade().delete_feed(request.view_args.get("id"))
            output.status = 1
        except Exception as e:
            output.error : Exception = e
            output.status = -1
        return output