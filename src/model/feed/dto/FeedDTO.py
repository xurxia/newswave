class FeedDTO():

    def __init__(self, id : int = 0, name : str = '', url : str = ''):
        self._id = id
        self._name = name
        self._url = url

    def _get_id(self) -> int:
        return self._id
    
    id = property (_get_id, None, None)

    def _get_name(self) -> str:
        return self._name
    
    def _set_name(self, name : str) -> None:
        self._name = name

    name = property(_get_name, _set_name, None)

    def _get_url(self) -> str:
        return self._url
    
    def _set_url(self, url : str) -> None:
        self._url = url

    url = property(_get_url, _set_url, None)


    