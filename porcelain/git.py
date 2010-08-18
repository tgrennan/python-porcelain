#! /usr/bin/python3.1

"""Function git() of class Porcelain.

"""

import sys
from subprocess import Popen, PIPE

def git(self, command, *args, **kw):
    """Run external GIT command.

    The keyword arguments are:
        stdin       (default is None)
        stdout      (default is PIPE)
        stderr      (default is sys.stderr)
    """
    stdin=None
    stdout=PIPE
    stderr=sys.stderr
    g = [ 'git' ]
    if self.git_dir:
        g.append('--git-dir=%s' % self.git_dir)
    if self.work_tree:
        g.append('--work-tree=%s' % self.work_tree)
    if command:
        g.append(command)
    for k_,v in kw.items():
        k = k_.replace('_','-')
        if k == 'stdin':
            stdin = v
        elif k == 'stdout':
            stdout = v
        elif k == 'stderr':
            stderr = v
        elif v == True or v == None:
            g.append('--%s' % k)
        else:
            g.append('--%s=%s' % (k, v))
    if len(args):
        g += args
    # print('git:', g)
    p = Popen(g, stdout=stdout, stderr=stderr)
    if stderr is PIPE:
        return p.communicate(stdin)[1].splitlines()
    if stdout is PIPE:
        return p.communicate(stdin)[0].splitlines()
    p.wait()
    return p.returncode
