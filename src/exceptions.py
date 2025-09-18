class GDriveLinkNotSetError(Exception):
    def __init__(self, message="An unexpected custom error occurred"):
        self.message = message
        super().__init__(self.message)

class CaptionIsNotCommandError(Exception):
    def __init__(self, message="An unexpected custom error occurred"):
        self.message = message
        super().__init__(self.message)

class InvalidFolderPathArgError(Exception):
    def __init__(self, message="Invalid folder path. Please follow the folder path argument convention, see /help for details."):
        self.message = message
        super().__init__(self.message)