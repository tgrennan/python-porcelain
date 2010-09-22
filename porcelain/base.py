#! /usr/bin/python3.1

"""Base classes of porcelain module.

"""

import sys
import os
import porcelain.git
import porcelain.post
import porcelain.publish

class Dict(dict):
    """Dict with scalar to list conversion

    If keyword already has scalar, convert and append to list.
    """
    def __init__(self):
        dict.__init__(self)

    def __setitem__(self, var, val):
        if var in self:
            cur = self[var]
            if isinstance(cur, list):
                self[var].append(val)
            else:
                dict.__setitem__(self, var, [cur, val])
        else:
            dict.__setitem__(self, var, val)

class Porcelain:
    """Base class for GIT Framework."""

    config = Dict()
    git = porcelain.git.git
    git1l = porcelain.git.git1l
    post = porcelain.post.post
    publish = porcelain.publish.publish

    def __init__(self, git_dir=None, work_tree=None):
        """Instantiate GIT framework."""

        self.git_dir = git_dir
        self.work_tree = work_tree
        if not git_dir:
            self.git_dir = self.git1l('rev-parse', '--git-dir')
        if not work_tree:
            self.work_tree = self.git1l('rev-parse', '--show-toplevel')
        for l in self.git('config', '--list'):
            try:
                k,v = l.split('=')
                self.config[k] = v
            except ValueError:
                self.config[l] = 'true'
        try:
            t = self.config['sendemail.aliasfiletype']
            f = self.config['sendemail.aliasesfile']
            for aka, addr in porcelain.post.mail_aliases[t](f):
                self.config['sendemail.alias.' + aka] = addr
        except KeyError:
            pass

