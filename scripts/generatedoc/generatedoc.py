def visiblename(name, all=None, obj=None):

    """Decide whether to show documentation on a variable."""

    # Certain special names are redundant or internal.

    # XXX Remove __initializing__?

    if name in {'__author__', '__builtins__', '__cached__', '__credits__',

                '__date__', '__doc__', '__file__', '__spec__',

                '__loader__', '__module__', '__name__', '__package__',

                '__path__', '__qualname__', '__slots__', '__version__'}:

        return 0

    if name.endswith("_swigregister"):
        return 0

    if name.startswith("__swig"):
        return 0

    # Private names are hidden, but special names are displayed.

    if name.startswith('__') and name.endswith('__'): return 1

    # Namedtuples have public fields and methods with a single leading underscore

    if name.startswith('_') and hasattr(obj, '_fields'):

        return True

    if all is not None:

        # only document that which the programmer exported in __all__

        return name in all

    else:

        return not name.startswith('_')

"""

This script generates a HTML doc from the pypylon installation

"""
if __name__ == '__main__':
    import pydoc
    pydoc.visiblename = visiblename
    from pypylon import pylon, genicam

    pydoc.writedoc(pylon)
    pydoc.writedoc(genicam)


