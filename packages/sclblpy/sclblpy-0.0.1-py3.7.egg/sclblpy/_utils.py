# Utility functions (internal)
from sclblpy import *
import inspect
import json


def __supported_model(obj) -> bool:
    """Checks whether the supplied model is supported.

    """
    global SUPPORTED_MODELS
    if not SUPPORTED_MODELS:
        try:
            with open(CURRENT_FOLDER+"/supported.json", "r") as f:
                SUPPORTED_MODELS = json.load(f)
                print("opening file...")
        except FileNotFoundError:
            raise ModelSupportError("Unable to find list of supported models.")

    print(SUPPORTED_MODELS)
    print(__get_model_name(obj))
    print(__get_model_package(obj))

    return True


def __get_model_package(obj):
    """Gets the package name of a model object.

    Args:
        obj: a fitted model object
    """
    mod = inspect.getmodule(obj)
    base, _sep, _stem = mod.__name__.partition('.')
    return base


def __get_model_name(obj):
    return type(obj).__name__


def __load_supported_models():
    print("loading supported models..")