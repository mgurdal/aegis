
class UserDefinedException(Exception):
    status: int
    title: str
    detail: str

    def __init__(self, **kwargs):
        assert self.status, "'status' attribute is required"
        assert self.title, "'title' attribute is required"
        assert self.detail, "'detail' attribute is required"
        self.title = self.title.format(**kwargs)
        self.detail = self.detail.format(**kwargs)
