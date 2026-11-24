import inspect

import raghu
from raghu import containers, graphs, linear, searching_sorting, trees

MODULES = [linear, searching_sorting, trees, graphs, containers]


def test_every_name_in_all_exists_on_package():
    for name in raghu.__all__:
        assert hasattr(raghu, name)
        assert getattr(raghu, name) is not None


def test_every_module_export_in_top_level_all():
    for mod in MODULES:
        for name in mod.__all__:
            assert name in raghu.__all__
            assert hasattr(raghu, name)
            assert getattr(raghu, name) is getattr(mod, name)


def test_every_public_class_and_function_exported_at_top_level():
    for mod in MODULES:
        for name, obj in inspect.getmembers(mod):
            if name.startswith("_"):
                continue
            if inspect.isclass(obj) or inspect.isfunction(obj):
                if obj.__module__ == mod.__name__:
                    assert name in raghu.__all__
                    assert hasattr(raghu, name)
                    assert getattr(raghu, name) is obj
