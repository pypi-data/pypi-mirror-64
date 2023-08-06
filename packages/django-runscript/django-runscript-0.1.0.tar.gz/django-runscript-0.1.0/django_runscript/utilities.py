from typing import Callable

from django.apps import apps
from django.utils.module_loading import import_string


def import_script(script_path: str) -> Callable:
    try:
        module_path, script_file = script_path.rsplit('.', 1)
    except ValueError:
        raise ImportError(f'{script_path} doesn\'t look like a module path')

    return import_string(f'{module_path}.scripts.{script_file}.run')


def import_script_lookup(script_path: str) -> Callable:
    script_lookup = [
        (import_string, f'{script_path}.run'), (import_script, script_path)
    ]

    for app in apps.get_app_configs():
        script_lookup.append((import_script, f'{app.module.__name__}.{script_path}'))

    for import_function, _script_path in script_lookup:
        try:
            return import_function(_script_path)
        except ImportError:
            pass

    raise ImportError(f'Cannot find {script_path}')
