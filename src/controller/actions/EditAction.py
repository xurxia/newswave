from src.controller.actions.Action import Action, Output, request
from src.model.feed.facade.FeedFacade import FeedFacade, FeedDTO

class EditAction(Action):

    def exec(self, request : request) -> Output:
        output = Output()
        try:
            output.vars["feed"] : FeedDTO = FeedFacade().get_feed(request.view_args.get("id"))
            output.status = 1
        except Exception as e:
            output.error : Exception = e
            output.status = -1
        return output