class Output():

    def __init__(self, status : int = 0, error : Exception = None, vars : dict = {}):
        self._status = status
        self._error = error
        self._vars = vars

    def _get_status(self) -> int:
        return self._status
    
    def _set_status(self, status : int) -> None:
        self._status = status

    status = property(_get_status, _set_status, None)

    def _get_error(self) -> Exception:
        return self._error
    
    def _set_error(self, error : Exception) -> None:
        self._error = error

    error = property(_get_error, _set_error, None)

    def _get_vars(self) -> dict:
        return self._vars
    
    def _set_vars(self, vars : dict) -> None:
        self._vars = vars

    vars = property(_get_vars, _set_vars, None)