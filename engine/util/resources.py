# Resource Managing
import os
from typing import AnyStr

APPLICATION_PATH: str
RESOURCE_PATH: str


def get_application_path():
    return APPLICATION_PATH


def get_resource_path():
    return RESOURCE_PATH


def set_application_path(path: AnyStr):
    # Set application path and concatenate resource path
    global APPLICATION_PATH
    global RESOURCE_PATH

    APPLICATION_PATH = path
    RESOURCE_PATH = os.path.join(APPLICATION_PATH, "resources")
