from pathlib import Path
from importlib import util
from typing import Union

from .tf_env import tf_env


def import_pyscript(modname: str, path: Union[str, Path]):
    """Import module (modname) from path python3.6+
    """
    spec = util.spec_from_file_location(modname, path)
    mod = util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
