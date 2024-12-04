from .logging import LoggerFactory

class BaseService:
    def __init__(self, use_logger: bool = True):
        if use_logger:
            self.logger = LoggerFactory().get_logger(self.__class__.__name__) 