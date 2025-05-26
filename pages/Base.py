from driver import Driver


class Base:
    """ Базовый класс """
    def __init__(self, dr):
        self.dr: Driver = dr