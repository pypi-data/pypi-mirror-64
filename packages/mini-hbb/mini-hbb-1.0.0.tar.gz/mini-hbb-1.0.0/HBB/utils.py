#!/usr/bin/env python
# 
# Copyright (c) 2006-2014 Hillstone Networks, Inc.
#

#
# Utils
#

from threading import Thread
import sys
import os
import glob

import json
import yaml

from .log import log


##############################################
## Threading
# Add collection for common thread
class HBBThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self._return = {"state": None, "exception": None}
    def run(self):
        if self._Thread__target is not None:
            try:
                self._return["state"] = self._Thread__target(*self._Thread__args,
                                                    **self._Thread__kwargs)
            except:
                self._return["exception"] = sys.exc_info()
    def join(self):
        Thread.join(self)
        return self._return


##############################################
## Reflection
# attach a class to an object
def attachClass(obj, cls):
    new_clsname = obj.__class__.__name__ + cls.__name__
    obj.__class__ = type(new_clsname, (obj.__class__, cls), {})


## factory facilities init a instance of a child class according to the specified attribute
def _get_subclass(cls, key, value):
    subclasses = _all_subclasses(cls)
    for scls in subclasses:
        if hasattr(scls, key) and (getattr(scls, key) == value):
            return scls
    log.debug("No subclass found:\n\tbase: %s\n\tcrit: %s=%s", cls.__name__, key, value)
    raise Exception("Unknown subclass.")


def _all_subclasses(cls):
    subclasses = cls.__subclasses__() + [g for s in cls.__subclasses__()
                                     for g in _all_subclasses(s)] 
    return subclasses


class ROClassPropertyDescriptor(object):
    """The read only class property which can only be accessed from class itself.
    Specificly used for testcase result instrumentation"""
    def __init__(self, fget):
        self.fget = fget
    
    def __get__(self, obj, klass):
        """Call the getter"""
        if obj is None:
            return self.fget.__get__(obj, klass)()
        else:
            # raise a AttributeError when called by instance
            raise AttributeError("'%s' object has no attribute '%s'" % (klass.__name__, self.fget.__name__))
    def __set__(self, obj, value):
        """Not setable"""
        raise AttributeError("Attribute '%s' is read only" % self.fget.__name__)


def roclassproperty(func):
    """The decorator for ROClassPropertyDescriptor"""
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ROClassPropertyDescriptor(func)

##############################################
## file facilities
def load_json(fileuri):
    """Load json file into a dict"""
    fd = open(fileuri, 'r')
    try:
        return json.load(fd)
    except Exception, e:
        raise e
    finally:
        fd.close()
    
def load_yaml(fileuri):
    """Load yaml file into a dict"""
    fd = open(fileuri, 'r')
    try:
        return yaml.load(fd)
    except Exception, e:
        raise e
    finally:
        fd.close()

# find all files with specific extension in a folder
def find_all_files(path, extension):
    if path.startswith("git@") or path.startswith("http://") or path.startswith("https://"):
        log.warn("Git repo not supported yet.")
        return []
    # 
    if os.path.isfile(path) and path.endswith(extension):
        return [path]
    else:
        # simply return the glob
        return glob.glob("/usr/*.%s" % extension)


def get_upload_folder():
    """Get the folder to store local files used for ftp upload/download"""
    # one folder for each process
    pname = "/tmp/HBB_%s" % os.getpid()
    if not os.path.isdir(pname):
        os.mkdir(pname)
    return pname


def get_host_ip():
    """Get the ip address of host, used for upload/download file"""
    ifname = 'eth0'
    return get_ip_address(ifname)


def get_ip_address(ifname):
    """Get the ip address of interface, used for upload/download file"""
    import socket
    import fcntl
    import struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])


def transfer_mac(mac):
    """Transfer MAC address format from xxxx.xxxx.xxxx to xx:xx:xx:xx:xx:xx"""
    mac = ''.join(mac.split('.'))
    rslt = ':'.join([mac[e:e+2] for e in range(0,11,2)])
    return rslt
