class AuthError (Exception):
    def __init__ (self, text):
        self.txt = text;
        
class APIError (Exception):
    def __init__ (self, text):
        self.txt = text;
        
class UploadError (Exception):
    def __init__ (self, text):
        self.txt = text;