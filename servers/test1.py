#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    test1

    Server Test

    :copyright: (c) 2011 by the Avelino Labs Team
    :author: Thiago Avelino
    :license: New BSD License
    :version: 0.1
"""
from fabric.api import env

def __init__():
    env.user = 'test1'
    env.user = 'root'
    env.password = 'lerolero'
    env.hosts = ['10.0.0.3']
    env.folder = '/home/avelino/'
