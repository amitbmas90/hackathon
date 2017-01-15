#!/usr/bin/env python
"""
Randomly generates and sends data to graphite endpoint
"""
import socket
import re
import random

def formatted(failed_list, alias):
    """
    Generates a format that collectd accepts
    :param failed_list: list of failed slots
    :param alias: alias of the hostname
    :return: string that collectd accepts
    """
    return "PUTVAL {}/smartalert/gauge interval={} N:{}".format(alias, 60, value)


def get_alias(host_name):
    """
    Generates alias from hostname. First part of the FQDN
    :param host_name: hostname of the system
    :return: alias
    """
    regex = re.compile(r'([^\.]+)\..*')
    match = regex.search(host_name)
    if match:
        return match.groups()[0]
    else:
        return host_name
def rand_int(a,b):
    return random.randint(a,b)


if __name__ == '__main__':

    host_name = socket.gethostname()

    alias=get_alias(host_name)
    value=rand_int(1000,1100)
    print formatted(value, alias)
