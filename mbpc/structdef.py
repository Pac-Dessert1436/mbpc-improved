from .utilities import MbpcSelf
from .interfaces import InterfaceError
from inspect import signature

def _StructBase(self):
    existing = self.__dict__.copy()

    @self.method
    def to_string() -> str:
        filtered = {}
        method_names = [name for name, func in self.__dict__.items()
                        if hasattr(func, '__name__') and func.__name__ in self.__dict__]
        for key, value in self.__dict__.items():
            if key not in [*existing, *method_names, "__classname__"]:
                filtered[key] = value
        return str(filtered)

    return self


_StructBase.__mbpctype__ = "struct"
_StructBase.__interfaces__ = []


def structdef(*interfaces):
    interfaces = list(interfaces)
    struct = _StructBase

    def mystruct(deco_struct):
        def mybase(*args, **kwargs):
            self = MbpcSelf()
            args = list(args)
            if args and type(args[0]) == type(self):
                self = args[0]
                args.pop(0)
            self.__dict__ |= struct(self).__dict__
            self.__classname__ = deco_struct.__name__
            deco_struct(self, *args, **kwargs)

            for interface in reversed(interfaces):
                for k in interface.__interface__.methods.keys():
                    if not k in self.__dict__:
                        raise InterfaceError(
                            f"Struct \"{self.__classname__}\" does not implement the interface \"{interface.__interface__.__interfacename__}\" (missing the method \"{k}\")."
                        )

                    if not signature(self.__dict__[k]) == interface.__interface__.methods[k]:
                        raise InterfaceError(
                            f"Struct \"{self.__classname__}\" does not implement the interface \"{interface.__interface__.__interfacename__}\" (incorrectly defining the method \"{k}\")."
                        )
            return self

        def method(f):
            mybase.__dict__[f.__name__] = f

        mybase.method = method
        mybase.__mbpctype__ = "struct"
        mybase.__interfaces__ = interfaces

        def initialize():
            for interface in reversed(interfaces):
                for k in interface.__methods__.keys():
                    if not k in mybase.__dict__:
                        raise InterfaceError(
                            f"Struct \"{deco_struct.__name__}\" does not implement the interface \"{interface.__interface__.__interfacename__}\" (missing the static method \"{k}\")."
                        )

                    if not signature(mybase.__dict__[k]) == interface.__methods__[k]:
                        raise InterfaceError(
                            f"Struct \"{deco_struct.__name__}\" does not implement the interface \"{interface.__interface__.__interfacename__}\" (incorrectly defining the static method \"{k}\")."
                        )
                    
        def clone():
            from copy import deepcopy
            return deepcopy(mybase.__dict__)

        mybase.init = initialize
        mybase.clone = clone
        return mybase
    return mystruct
