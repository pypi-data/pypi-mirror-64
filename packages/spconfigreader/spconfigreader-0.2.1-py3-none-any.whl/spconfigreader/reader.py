import confuse
from os import environ
import inspect

primitive = (int, float, complex, str, bool)

__configfile__ = "config.yml"

config = None


class MissingPathError(Exception):
    pass


class NoValueError(Exception):
    pass


def _getConfig():
    global config

    if config is None:
        config = confuse.Configuration('config', read=False)
        config.set_file(__configfile__)

    return config


def _buildPath(key: str, name: str) -> str:
    if key and name:
        return "{}.{}".format(key, name)
    elif key:
        return "{}".format(key)
    elif name:
        return "{}".format(name)
    else:
        return None


def _getFromENV(path: str):
    return environ.get(path.replace('.', '_').upper())


def _getFromYAML(path: str):
    val = _getConfig()

    for k in path.split("."):
        val = val[k]

    return val


def get(key: str, name: str, default: str = None):
    path = _buildPath(key, name)

    val = _getFromENV(path)
    if val is not None:
        return val

    try:
        val = _getFromYAML(path).get()
        if val is not None:
            return val

    except confuse.NotFoundError:
        pass

    if default is not None:
        return default

    raise NoValueError("no value for {} defined!".format(path))


def _attributesOfObject(obj: object) -> list:
    attributes = [attr for attr in vars(
        type(obj))["__annotations__"] if attr[0] is not '_']
    attributes += [attr for attr in vars(type(obj)) if attr[0] is not '_']
    attributes += [attr for attr in vars(obj) if attr[0] is not '_']

    return list(dict.fromkeys(attributes))


def _isPrimitive(t: type) -> bool:
    return t in primitive


def _getAttrVal(obj: object, attr: str):

    val = vars(obj).get(attr, None)
    if val is not None:
        return val

    return vars(type(obj)).get(attr, None)


def _isObject(obj: object, attr: str) -> bool:

    val = vars(obj).get(attr, None)
    if val is not None and not _isPrimitive(type(val)):
        return True

    val = vars(type(obj)).get(attr, None)
    if val is not None and not _isPrimitive(type(val)):
        return True

    return False


def getObject(obj: object, path: str = None) -> object:

    if path is not None:
        basepath = path
    else:
        try:
            basepath = obj.__path__
        except(AttributeError):
            raise MissingPathError(
                "Attribute __path__ is missing in given Object")

    attributes = _attributesOfObject(obj)

    for attr in attributes:
        if _isObject(obj, attr):
            vars(obj)[attr] = getObject(_getAttrVal(
                obj, attr), "{}.{}".format(basepath, attr))
        else:
            vars(obj)[attr] = get(basepath, attr, _getAttrVal(obj, attr))

    return obj
