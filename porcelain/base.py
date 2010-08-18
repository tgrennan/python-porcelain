#! /usr/bin/python3.1

"""Base classes of porcelain module.

"""

import sys
import os
import re
import collections

# FIXME! add parsers for: mailrc, pine, elm and gnus type aliases
def _MuttAlias(fn='/dev/null'):
    """Return list of [alias, address] parsed from named Mutt file."""
    aliases = []
    p = re.compile(r'alias[ \t]+([^ \t]+)[ \t]+([^\n]+)')
    with open(fn, 'r') as f:
        for l in f:
            m = p.match(l)
            if m:
                aliases.append([m.group(1),  m.group(2)])
    return aliases

class _Superdict(dict):
    """Dict with scalar to list conversion

    If keyword already has scalar, convert and append to list.
    """
    def __init__(self):
        dict.__init__(self)

    def __setitem__(self, var, val):
        if var in self:
            cur = self[var]
            if type(cur) is list:
                self[var].append(val)
            else:
                dict.__setitem__(self, var, [cur, val])
        else:
            dict.__setitem__(self, var, val)

class _Config(_Superdict):
    """Dictionary created from parsed output of `git config --list`

    Lines without equal sign ('=') result in the named variable assigned
    boolean "true".
    """
    def __init__(self, lines):
        _Superdict.__init__(self)
        for var,val \
        in [[[l, 'true'], l.decode().split('=')][b'=' in l] for l in lines]:
            self[var] = val
        try:
            t = self['sendemail.aliasfiletype']
            f = self['sendemail.aliasesfile']
            v = {'mutt': _MuttAlias}
            for aka, addr in v[t](f):
                self['sendemail.alias.' + aka] = addr
        except KeyError:
            pass

class Options(_Superdict):
    """Pop leading options from command argument list"""
    def __init__(self, args):
        _Superdict.__init__(self)
        while len(args) and args[0].startswith('--'):
            opt = args.pop(0)[2:]
            if not len(opt):
                break       # interpret '--' as end of options
            try:
                name, val = opt.split('=')
                name_ = name.replace('-','_')
                self[name_] = val
            except ValueError:
                name_ = opt.replace('-','_')
                if not len(args) or args[0].startswith('--'):
                    self[name_] = True
                else:
                    self[name_] = args.pop(0)

class Porcelain:
    """Base class for GIT Framework.

    """
    def __init__(self, git_dir=None, work_tree=None):
        """Instantiate GIT framework.

        The arguments are:
            git-dir     Repository directory (default is $PWD/.git)
            work-tree   Work tree directory (default is $PWD)
        """
        self.git_dir = git_dir
        self.work_tree = work_tree
        self.config = _Config(self.git('config', '--list'))

