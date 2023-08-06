from collections.abc import Mapping

class DefaultValue(object):
    def __init__(self, value_or_fn):
        self.value_or_fn = value_or_fn

    def resolve(self):
        if callable(self.value_or_fn):
            return self.value_or_fn()
        else:
            return self.value_or_fn

DEFAULT_PLACEHOLDER = DefaultValue(None)

def update(target, updater):
    """Deep update of dict target using updater. 
    
    The special DEFAULT_PLACEHOLDER object allows to set default values"""
    for key, value in updater.items():
        if isinstance(value, Mapping):
            target[key] = update(target.get(key, {}), value)
        else:
            if is_default(value) and key in target:
                # Do no replace existing value with the default placeholder
                pass
            else:
                target[key] = value
    return target

def is_default(value):
    return isinstance(value, DefaultValue)

def replace_defaults(target):
    for key, value in target.items():
        if isinstance(value, Mapping):
            replace_defaults(value)
        else:
            if is_default(value):
                target[key] = value.resolve()
    return target
