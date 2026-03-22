from .interfacedef import interfacedef


@interfacedef()
def Hashable(self):
    @self.method
    def hashcode() -> int: ...


@interfacedef()
def Equatable(self):
    @self.method
    def equals(object) -> bool: ...
