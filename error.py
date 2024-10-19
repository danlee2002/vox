from tokens import Tokens

class RuntimeException(RuntimeError):
    def __init__(self, token: Tokens, message: str):
        super().__init__(message)
        self.token = token
class ParseError(RuntimeError):
    pass 