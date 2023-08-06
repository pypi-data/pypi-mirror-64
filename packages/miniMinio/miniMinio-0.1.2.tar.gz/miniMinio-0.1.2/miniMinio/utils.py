import datetime
import os
import time


def get_attributes_minio(attributes, s3_object, store):
    attribute_list = []
    for attribute in attributes:
        attribute_list.append(getattr(s3_object, attribute))
    store.append(tuple(attribute_list))
    return store


def get_attributes_local(files, path, store, filter_object):
    for name in files:
        mtime = os.path.getmtime(path)
        if "excel" in filter_object:
            filename, filename_ext = os.path.splitext(name)
            if (filename_ext == ".xlsx") or (filename_ext == ".xls"):
                store.append((os.path.join(path, name),
                              datetime.datetime.strptime(time.ctime(mtime), "%a %b %d %H:%M:%S %Y")))
        else:
            store.append((os.path.join(path, name),
                          datetime.datetime.strptime(time.ctime(mtime), "%a %b %d %H:%M:%S %Y")))
    return store


def path_leaf_last(path):
    head, tail = os.path.split(path)
    head = os.path.basename(head)
    return tail or head


def get_attributes_single_local(path, store):
    store.append((path,
                  datetime.datetime.strptime(time.ctime(os.path.getmtime(path)), "%a %b %d %H:%M:%S %Y")))
    return store
