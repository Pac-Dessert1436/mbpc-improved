from .interfaces import InterfaceError
from inspect import signature


def _Interface():
    def interface(): return ...
    interface.methods = {}

    def method(func):
        interface.methods[func.__name__] = signature(func)

    interface.method = method
    return interface


def interfacedef(*super_interfaces):
    interface = _Interface()

    for super_interface in reversed(super_interfaces):
        interface.__dict__ |= super_interface.__interface__.__dict__

    def wrapper(decorated_interface):
        decorated_interface(interface)
        interface.__interfacename__ = decorated_interface.__name__

        def mybase(*args, **kwargs):
            raise InterfaceError("Cannot initialize an interface object.")

        mybase.__interface__ = interface
        mybase.__mbpctype__ = "interface"

        mybase.__methods__ = {}

        def method(func):
            mybase.__methods__[func.__name__] = signature(func)

        mybase.method = method

        return mybase
    return wrapper
