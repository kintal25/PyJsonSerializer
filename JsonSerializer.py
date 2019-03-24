import json
import datetime
import os


def ToJson(obj):
    return json.dumps(obj, default=_ObjToDict)


def FromJson(jsonString):
    return json.loads(jsonString, object_hook=_DictToObj)


def ToJsonFile(obj, filepath):
    with open(filepath, 'w') as jfile:
        jfile.writelines(ToJson(obj))


def FromJsonFile(filepath):
    result = None
    if not os.path.exists(filepath):
        raise FileNotFoundError("File path {} wasn't found".format(filepath))

    with open(filepath, 'r') as jfile:
        result = FromJson(jfile.read())
    return result


def _DictToObj(our_dict):
    """
    Function that takes in a dict and returns a custom object associated with the dict.
    This function makes use of the "__module__" and "__class__" metadata in the dictionary
    to know which object type to create.
    """
    if "__class__" in our_dict:
        # Pop ensures we remove metadata from the dict to leave only the instance arguments
        class_name = our_dict.pop("__class__")

        # Get the module name from the dict and import it
        module_name = our_dict.pop("__module__")

        # We use the built in __import__ function since the module name is not yet known at runtime
        module = __import__(module_name)

        # Get the class from the module
        class_ = getattr(module, class_name)

        # Use dictionary unpacking to initialize the object
        obj = class_(**our_dict)
        return obj

    elif "__type__" in our_dict:
        # Decoding datetime types
        if type == "datetime":
            dateobj = datetime.datetime(**our_dict)
            return dateobj
        elif type == "date":
            dateobj = datetime.datetime(**our_dict).date
            return dateobj
    else:
        return our_dict


def _ObjToDict(obj):
    """
    A function takes in a custom object and returns a dictionary representation of the object.
    This dict representation includes meta data such as the object's module and class names.
    """

    # Handling datetime types
    if isinstance(obj, datetime.datetime):
        return {
            '__type__': 'datetime',
            'year': obj.year,
            'month': obj.month,
            'day': obj.day,
            'hour': obj.hour,
            'minute': obj.minute,
            'second': obj.second,
            'microsecond': obj.microsecond,
        }

    elif isinstance(obj, datetime.date):
        return {
            '__type__': 'date',
            'year': obj.year,
            'month': obj.month,
            'day': obj.day
        }

    #  Populate the dictionary with object meta data
    obj_dict = {
        "__class__": obj.__class__.__name__,
        "__module__": obj.__module__
    }

    #  Populate the dictionary with object properties
    obj_dict.update(obj.__dict__)
    return obj_dict
