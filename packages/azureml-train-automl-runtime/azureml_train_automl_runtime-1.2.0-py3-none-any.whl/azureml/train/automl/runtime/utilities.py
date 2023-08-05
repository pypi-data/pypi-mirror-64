# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Contains utility methods used in automated ML in Azure Machine Learning."""
from typing import Union, Optional
from types import ModuleType
import importlib
import importlib.util
import importlib.abc
import logging
import os
import numpy as np

from azureml.automl.core.shared import constants
from azureml.automl.core.shared.exceptions import InvalidArgumentException
from azureml.automl.runtime.shared.types import DataSingleColumnInputType
from azureml.train.automl.exceptions import ConfigException, FileNotFoundException
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings


def _load_user_script(script_path: str, logger: logging.Logger, calling_in_client_runtime: bool = True) -> ModuleType:
    #  Load user script to get access to GetData function
    logger.info('Loading data using user script.')

    module_name, module_ext = os.path.splitext(os.path.basename(script_path))
    if module_ext != '.py':
        raise ConfigException.create_without_pii('The provided user script was not a Python file.')
    spec = importlib.util.spec_from_file_location('get_data', script_path)
    if spec is None:
        if calling_in_client_runtime:
            raise ConfigException.create_without_pii('The provided user script path does not exist.')
        else:
            raise FileNotFoundException.create_without_pii('The provided user script path does not exist.',
                                                           target="LoadUserScript")

    module_obj = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ConfigException.create_without_pii('The provided user script is a namespace package, '
                                                 'which is not supported.')

    # exec_module exists on 3.4+, but it's marked optional so we have to assert
    assert isinstance(spec.loader, importlib.abc.Loader)
    assert spec.loader.exec_module is not None
    try:
        spec.loader.exec_module(module_obj)
    except FileNotFoundError:
        if calling_in_client_runtime:
            raise ConfigException.create_without_pii('The provided user script path does not exist.')
        else:
            if not os.path.exists(script_path):
                raise FileNotFoundException.create_without_pii('The provided user script path does not exist.',
                                                               target="LoadUserScript")
            else:
                raise ConfigException.create_without_pii(
                    'The provided user script references files that are not in the project folder.')
    except Exception as e:
        raise InvalidArgumentException('Exception while executing user script.',
                                       target="module_obj",
                                       reference_code="_load_user_script.module_obj.exception",
                                       has_pii=False)

    if not hasattr(module_obj, 'get_data'):
        raise ConfigException.with_generic_msg('The provided user script does not implement get_data().')

    return module_obj
