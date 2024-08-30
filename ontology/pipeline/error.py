class BuildError(Exception):
    def __init__(self, title: str, message: str = None, warning: bool = False):
        self.title = title
        self.message = message
        self.warning = warning

    def print(self):
        if self.warning:
            print("\033[93m" + self.title + "\033[0m")
        else:
            print("\033[91m" + self.title + "\033[0m")

        if self.message is not None:
            print("\033[90m" + self.message + "\033[0m")
