from src.controller.actions.Action import Action, Output, Request
from src.model.feed.facade.FeedFacade import FeedFacade, FeedDTO
from src.model.exception.ModelException import ModelException

class EditAction(Action):

    def exec(self, request : Request) -> Output:
        output = Output()
        try:
            id = request.view_args.get("id")
            feed : FeedDTO = FeedFacade().get_feed(id)
            if feed is not None:
                output.vars["feed"] = feed
                output.status = 1
            else:
                raise ModelException(f'Feed {id} does not exist')
        except Exception as e:
            output.error : Exception = e
            output.status = -1
        return output