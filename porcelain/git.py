#! /usr/bin/python3.1

"""Function git() of class Porcelain.

"""

import sys
from subprocess import Popen, PIPE

def git(self, command, *args, stdin=None, stdout=PIPE, stderr=sys.stderr, **kw):
    """Run external GIT command."""
    g = [ 'git' ]
    if self.git_dir:
        g.append('--git-dir=%s' % self.git_dir)
    if self.work_tree:
        g.append('--work-tree=%s' % self.work_tree)
    if command:
        g.append(command)
    for k_,v in kw.items():
        k = k_.replace('_','-')
        if v == True or v == None:
            g.append('--%s' % k)
        else:
            g.append('--%s=%s' % (k, v))
    if len(args):
        g += args
    p = Popen(g, stdout=stdout, stderr=stderr)
    if stderr is PIPE:
        return p.communicate(stdin)[1].decode().splitlines()
    if stdout is PIPE:
        return p.communicate(stdin)[0].decode().splitlines()
    p.wait()
    return p.returncode

def git1l(self, command, *args, **kw):
    """Return first line of executed GIT command or None."""
    try:
        return self.git(command, *args, **kw)[0]
    except IndexError:
        return None
