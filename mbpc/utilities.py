class InterfaceError(Exception):
    pass


def MbpcSelf():
    def self(): pass

    def method(f):
        self.__dict__[f.__name__] = f

    self.method = method
    return self
