import pkgutil
import importlib
import inspect
from level.base_level import BaseLevel
from level.ascii_level import AsciiLevel


def discover_levels(package_name="level"):
    pkg = importlib.import_module(package_name)
    found = []

    for modinfo in pkgutil.iter_modules(pkg.__path__):
        name = modinfo.name

        # only load level*.py
        if not name.startswith("level"):
            continue

        # skip non-level files
        if name in ("base_level", "ascii_level", "registry"):
            continue

        module = importlib.import_module(f"{package_name}.{name}")

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if not issubclass(obj, BaseLevel):
                continue

            # 🔑 skip abstract/helper classes
            if obj in (BaseLevel, AsciiLevel):
                continue

            found.append(obj)

    # 🔑 ensure deterministic order: level1, level2, ...
    found.sort(key=lambda cls: cls.__module__)

    return found
