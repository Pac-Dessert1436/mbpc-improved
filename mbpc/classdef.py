from .utilities import InterfaceError, MbpcSelf
from inspect import signature


def _ClassBase(self):
    @self.method
    def to_string(debug: bool = False):
        return self.__dict__ if debug else f"{self.__classname__} object"

    return self


_ClassBase.__mbpctype__ = "class"
_ClassBase.__interfaces__ = []


def classdef(super_cls=_ClassBase, *interfaces):
    interfaces = list(interfaces)
    if super_cls.__mbpctype__ == "interface":
        interfaces.insert(0, super_cls)
        super_cls = _ClassBase
    elif super_cls.__mbpctype__ == "struct":
        raise InterfaceError(
            f"Cannot inherit from a struct (super_cls: {super_cls.__name__}). Structs do not support inheritance."
        )
    interfaces.extend(super_cls.__interfaces__)

    def myclass(deco_class):
        def mybase(*args, **kwargs):
            self = MbpcSelf()
            args = list(args)
            if args and type(args[0]) == type(self):
                self = args[0]
                args.pop(0)

            def initialize(*args, **kwargs):
                self.__dict__ |= super_cls(self, *args, **kwargs).__dict__

            def super(): pass
            for name in self.__dict__:
                super.__dict__[name] = self.__dict__[name]
            super.init = initialize
            self.super = super

            self.__classname__ = deco_class.__name__
            deco_class(self, *args, **kwargs)

            for interface in reversed(interfaces):
                for k in interface.__interface__.methods.keys():
                    if not k in self.__dict__:
                        raise InterfaceError(
                            f"Class \"{self.__classname__}\" does not implement the interface \"{interface.__interface__.__interfacename__}\" (missing the method \"{k}\")."
                        )

                    if not signature(self.__dict__[k]) == interface.__interface__.methods[k]:
                        raise InterfaceError(
                            f"Class \"{self.__classname__}\" does not implement the interface \"{interface.__interface__.__interfacename__}\" (incorrectly defining the method \"{k}\")."
                        )
            return self

        def method(f):
            mybase.__dict__[f.__name__] = f

        mybase.__dict__ = super_cls.__dict__ | mybase.__dict__
        mybase.method = method
        mybase.__mbpctype__ = "class" if super_cls.__mbpctype__ == _ClassBase else "struct"
        mybase.__interfaces__ = interfaces

        def initialize():
            for interface in reversed(interfaces):
                for k in interface.__methods__.keys():
                    if not k in mybase.__dict__:
                        raise InterfaceError(
                            f"Class \"{deco_class.__name__}\" does not implement the interface \"{interface.__interface__.__interfacename__}\" (missing the static method \"{k}\")."
                        )

                    if not signature(mybase.__dict__[k]) == interface.__methods__[k]:
                        raise InterfaceError(
                            f"Class \"{deco_class.__name__}\" does not implement the interface \"{interface.__interface__.__interfacename__}\" (incorrectly defining the static method \"{k}\")."
                        )

        def clone():
            from copy import deepcopy
            return deepcopy(mybase.__dict__)

        mybase.init = initialize
        mybase.clone = clone
        return mybase
    return myclass
