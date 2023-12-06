from enum import Enum


class Browsers(Enum):
    Chrome = 'Chrome'
    FireFox = 'FireFox'

class Platform(Enum):
    WINDOWS = 'Windows'
    Linux = 'Linux'
    MACOS = 'MacOS'

ELEMENT_WAIT_TIMEOUT = 5

STATUS_OK = 200