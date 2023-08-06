from typing import Callable, List

from django.apps import apps
from django.utils.module_loading import import_string


def apps_lookup(template: str) -> List[str]:
    return [template % a.module.__name__ for a in apps.get_app_configs()]


def import_script(script_path: str) -> Callable:
    lookup_paths, module_path, script_name = [], None, script_path

    if '.' in script_name:
        module_path, script_name = script_path.rsplit('.', 1)

    if module_path is None:
        lookup_paths += apps_lookup(f'%s.scripts.{script_name}.run')
        lookup_paths += apps_lookup(f'%s.scripts.{script_name}')
    else:
        lookup_paths.append(f'{module_path}.{script_name}.run')
        lookup_paths.append(f'{module_path}.{script_name}')

        lookup_paths.append(f'{module_path}.scripts.{script_name}.run')
        lookup_paths.append(f'{module_path}.scripts.{script_name}')

        lookup_paths += apps_lookup(f'%s.{module_path}.scripts.{script_name}.run')
        lookup_paths += apps_lookup(f'%s.{module_path}.scripts.{script_name}')

    for lookup_path in lookup_paths:
        try:
            run_script = import_string(lookup_path)
            assert isinstance(run_script, Callable)
        except (ImportError, AssertionError):
            pass
        else:
            return run_script

    raise ImportError(f'Cannot find {script_path}')
