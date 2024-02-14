class FeedDTO():

    def __init__(self, id : int = 0, name : str = '', url : str = '', etag : str = ''):
        self._id : int = id
        self._name : str = name
        self._url : str = url
        self._etag : str = etag

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

    def _get_etag(self) -> str:
        return self._etag
    
    def _set_etag(self, etag : str) -> None:
        self._etag = etag

    etag = property(_get_etag, _set_etag, None)
    