class GDriveLinkNotSetError(Exception):
    def __init__(self, message="An unexpected custom error occurred"):
        self.message = message
        super().__init__(self.message)