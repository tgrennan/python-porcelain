import sys
import re
from email.mime.text import MIMEText
from subprocess import PIPE

def publish(self, dry_run=False, push_log=None, **post):
    """Push updates and send request-pull message.

        dry-run     Don't send updates or mail message.
        push-log    Parse output of earlier update.

    See also:
        post
    """

    assert self.git_dir
    git_dir = self.git_dir if self.git_dir else '.git'
    if push_log:
        with open(push_log) as f:
            log = f.readlines(2048)
    elif dry_run:
        log = self.git('push', '--dry-run', stderr=PIPE)
    else:
        log = self.git('push', stderr=PIPE)
    baseref = {}
    p = re.compile(r'[ \t]+(\w+)\.\.\w+[ \t]+.* -> (.*)$')
    for l in log:
        m = p.match(l)
        if m:
            baseref[m.group(2)] = m.group(1)
    for name, base in baseref.items():
        try:
            remote = self.config['branch.' + name + '.remote']
            url = self.config['remote.' + remote + '.url']
        except KeyError:
            continue
        head = self.git1l('rev-parse', '--verify', '%s^0' % name)
        merge = self.git1l('merge-base', base, head)
        cmsg = self.git1l('log', '--format=%s', '%s^..%s' % (base, base))
        body = ['I updated "%s" in,' % name]
        body.append('<%s>'% url)
        body.append('')
        body.append('with these changes since 0x%s,' % base)
        body.append('"%s"' % cmsg)
        body.append('')
        body += self.git('shortlog', '-n', '-e', '-w78,1,8', '^'+base, head)
        body += self.git('diff', '-M', '--stat', base, '%s..%s' % (merge, head))
        self.post(dry_run,
                subject='request pull of "%s"' % name,
                text='\n'.join(body),
                **post)
