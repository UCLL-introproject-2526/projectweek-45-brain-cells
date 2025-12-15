import pkgutil
import importlib
import inspect
from level.base_level import BaseLevel

def discover_levels(package_name="level"):
    """
    Auto-load modules named level*.py inside the level package
    and collect subclasses of BaseLevel.
    Returns: list[type[BaseLevel]]
    """
    pkg = importlib.import_module(package_name)
    found = []

    for modinfo in pkgutil.iter_modules(pkg.__path__):
        name = modinfo.name
        if not name.startswith("level"):
            continue
        if name in ("level_manager", "registry", "base_level", "ascii_level"):
            continue

        module = importlib.import_module(f"{package_name}.{name}")

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseLevel) and obj is not BaseLevel:
                # avoid importing helper base classes like AsciiLevel if desired
                if obj.__name__ in ("AsciiLevel",):
                    continue
                found.append(obj)

    # sort nicely by class name
    found.sort(key=lambda c: c.__name__)
    return found
