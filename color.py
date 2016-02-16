
class colors:
    ERROR = '\033[91m'
    NORMAL = '\033[0m'
    WARNING = '\033[93m'
    OTHER = '\033[92m'


class out:
    def err(message):
        print(colors.ERROR + message + colors.NORMAL)

    def log(message):
        print(colors.OTHER + message + colors.NORMAL)

    def warning(message):
        print(colors.WARNING + message + colors.NORMAL)
