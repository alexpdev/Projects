


DEFAULT = {
    "user": "password"
    }



class AuthManager:
    def __init__(self,fd=None):
        self.path = fd
        self.credentials = DEFAULT

    def load(self):
        if not self.path:
