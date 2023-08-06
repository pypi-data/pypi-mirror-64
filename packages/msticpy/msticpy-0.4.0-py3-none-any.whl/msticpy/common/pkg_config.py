# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Package configuration reader.

Reads default configuration from package file `msticpyconfig.yaml`.
Optionally reads custom configuration from file specified in environment
variable `MSTICPYCONFIG`. If this is not defined the package will look for
a file `msticpyconfig.yaml` in the current directory.

Default settings are accessible as an attribute `default_settings`.
Custom settings are accessible as an attribute `custom_settings`.
Consolidated settings are accessible as an attribute `settings`.

"""
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Callable

import pkg_resources
import yaml
from yaml.error import YAMLError

from .utility import MsticpyConfigException
from .._version import VERSION

__version__ = VERSION
__author__ = "Ian Hellen"

_CONFIG_FILE: str = "msticpyconfig.yaml"
_CONFIG_ENV_VAR: str = "MSTICPYCONFIG"

# pylint: disable=invalid-name
default_settings: Dict[str, Any] = {}
custom_settings: Dict[str, Any] = {}
settings: Dict[str, Any] = {}


def _get_current_config() -> Callable[[Any], Optional[str]]:
    """Closure for holding path of config file."""
    _current_conf_file: Optional[str] = None

    def _current_config(file_path: Optional[str] = None) -> Optional[str]:
        nonlocal _current_conf_file
        if file_path is not None:
            _current_conf_file = file_path
        return _current_conf_file

    return _current_config


_CURRENT_CONF_FILE = _get_current_config()


def current_config_path() -> Optional[str]:
    """
    Return the path of the current config file, if any.

    Returns
    -------
    Optional[str]
        path of the current config file

    """
    return _CURRENT_CONF_FILE(None)


def refresh_config():
    """Re-read the config settings."""
    # pylint: disable=global-statement
    global default_settings, custom_settings, settings
    default_settings = _get_default_config()
    custom_settings = _get_custom_config()
    settings = _consolidate_configs(default_settings, custom_settings)


def get_config_path(elem_path: str) -> Any:
    """
    Return setting item for path.

    Parameters
    ----------
    elem_path : str
        Path to setting item expressed as dot-separated
        string

    Returns
    -------
    Any
        The item at the path location.

    """
    path_elems = elem_path.split(".")
    cur_node = settings
    for elem in path_elems:
        cur_node = cur_node.get(elem, None)
        if cur_node is None:
            raise KeyError(f"{elem} value of {elem_path} is not a valid path")
    return cur_node


def _read_config_file(config_file: str) -> Dict[str, Any]:
    """
    Read a yaml config definition file.

    Parameters
    ----------
    config_file : str
        Path to yaml config file

    Returns
    -------
    Dict
        Configuration settings

    """
    if Path(config_file).is_file():
        with open(config_file) as f_handle:
            # use safe_load instead of load
            try:
                return yaml.safe_load(f_handle)
            except YAMLError as yml_err:
                raise MsticpyConfigException(
                    f"Error reading config file {config_file}", yml_err
                )
    return {}


def _consolidate_configs(
    def_config: Dict[str, Any], cust_config: Dict[str, Any]
) -> Dict[str, Any]:
    resultant_config = {}
    resultant_config.update(def_config)

    _override_config(resultant_config, cust_config)
    return resultant_config


def _override_config(base_config: Dict[str, Any], new_config: Dict[str, Any]):
    for c_key, c_item in new_config.items():
        if c_item is None:
            continue
        if isinstance(base_config.get(c_key), dict):
            _override_config(base_config[c_key], new_config[c_key])
        else:
            base_config[c_key] = new_config[c_key]


def _get_default_config():
    # When called from a unit test msticpy is a level above the package root
    # so the first call produces an invalid path
    # return the actual path - pkgpath/msticpy/filename.yaml or just
    # pkgpath/filename.yaml. So we test it as we go
    conf_file = None
    top_module = _get_top_module()
    try:
        conf_file = pkg_resources.resource_filename(top_module, _CONFIG_FILE)
        if not Path(conf_file).is_file():
            conf_file = pkg_resources.resource_filename(
                top_module, "msticpy/" + _CONFIG_FILE
            )
    except ModuleNotFoundError:
        pass
    if not conf_file or not Path(conf_file).is_file():
        # if all else fails we try to find the package default config somewhere
        # in the package tree - we use the first one we find
        pkg_paths = sys.modules[top_module]
        if pkg_paths:
            conf_file = next(Path(pkg_paths.__path__[0]).glob("**/" + _CONFIG_FILE))
    if conf_file:
        return _read_config_file(conf_file)
    return {}


def _get_custom_config():
    config_path = os.environ.get(_CONFIG_ENV_VAR, None)
    if config_path and Path(config_path).is_file():
        _CURRENT_CONF_FILE(str(Path(config_path).resolve()))
        return _read_config_file(config_path)

    if Path(_CONFIG_FILE).is_file():
        _CURRENT_CONF_FILE(str(Path(".").joinpath(_CONFIG_FILE).resolve()))
        return _read_config_file(_CONFIG_FILE)
    return {}


def _get_top_module():
    module_path = __name__.split(".")
    top_module = __name__
    for idx in range(1, len(module_path)):
        test_module = ".".join(module_path[:-idx])
        if test_module in sys.modules:
            top_module = test_module
        else:
            break
    return top_module


# read initial config when first imported.
refresh_config()
