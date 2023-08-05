# -*- coding: utf-8 -*-


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattribute__ = dict.__getitem__


def dict_to_object(dictObj):
    """

    :param dictObj: dictObj
    :return: obj
    """
    if not isinstance(dictObj, dict):
        return dictObj
    inst = Dict()
    for k, v in dictObj.items():
        inst[k] = dict_to_object(v)
    return inst
