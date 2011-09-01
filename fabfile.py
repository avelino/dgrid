#!/usr/bin/python
# -*- coding: utf-8 -*-
#
"""
    fabfile

    Servers deploy dgird

    :copyright: (c) 2011 by the Avelino Labs Team
    :author: Thiago Avelino
    :license: New BSD License
    :version: 0.1
"""


import datetime
from fabric.api import *
from fabric.operations import local
from fabric.operations import put
from fabric.operations import get

from servers.test1 import __init__ as test1


# globals
env.project_name = 'dgrid'
env.use_photologue = False
date = datetime.datetime.today()
_date = "%s-%s-%s-%s-%s-%s" % (date.year,
        date.month,
        date.day,
        date.hour,
        date.minute,
        date.second)


def rm(path, _local=False):
    if _local:
        local("rm -rf %s" % path)
    else:
        run("rm -rf %s" % path)


def uptime():
    run('uptime')


def deploy(path):
    "Deploy local for remote"

    if settings(warn_only=True):
        # create tar local
        _open = "cd %s" % path
        _pull = "git pull origin master"
        _git = "git archive --format=tar master | gzip > ~/dgrid_deploy-%s.tar.gz" % env.user
        local("%s && %s && %s" % (_open, _pull, _git))

        # get tar remote for local
        _ropen = "cd %s" % env.folder
        run("%s && tar -zcf dgrid_bkp-%s-%s.tar.gz %s" % (_ropen,
            env.user,
            _date,
            env.folder))
        get("%sdgrid_bkp-%s-%s.tar.gz" % (env.folder,
            env.user,
            _date),
            "~/dgrid_bkp-%s-%s.tar.gz" % (env.user, _date))

        _folder_deploy = "%s../%s_deploy/" % (env.folder, env.name)
        test = run("mkdir %s" % _folder_deploy)
        rm("%s*" % _folder_deploy)

        # send tar local for remote
        put("~/dgrid_deploy-%s.tar.gz" % env.user, _folder_deploy)

        # open tar remote and remove tar remote
        _rfile = "%sdgrid_deploy-%s.tar.gz" % (_folder_deploy, env.user)
        _rtar = "tar -xf %s" % _rfile
        _ropen_folder_deploy = "cd %s" % _folder_deploy
        run("%s && %s" % (_ropen_folder_deploy, _rtar))

        rm("%s*" % env.folder)
        run("mv %s* %s" % (_folder_deploy, env.folder))

        # remove tar local
        rm("~/dgrid_deploy-%s.tar.gz" % env.user, True)
        rm(_folder_deploy)
