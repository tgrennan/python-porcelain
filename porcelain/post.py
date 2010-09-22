import sys
import re
import pydoc
from smtplib import SMTP
from email.message import Message
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class _MuttAliases(list):
    def __init__(self,fn='/dev/null'):
        """List of [alias, address] parsed from named Mutt file."""
        list.__init__(self)
        p = re.compile(r'alias[ \t]+([^ \t]+)[ \t]+([^\n]+)')
        with open(fn, 'r') as f:
            for l in f:
                m = p.match(l)
                if m:
                    self.append([m.group(1),  m.group(2)])

# FIXME! add parsers for: mailrc, pine, elm and gnus type aliases
mail_aliases = {'mutt': _MuttAliases}

def post(self,
        dry_run=False,
        smtpserver=None,
        name=None,
        email=None,
        to=None,
        cc=None,
        bcc=None,
        subject=None,
        text=None,
        filename=None,
        attach=None):
    """Emulate git-send-mail.

        dry-run     Print, don't send message.
        smtpserver  Default is 'localhost'
        name        From name.
        email       Return address.
        to          Mail addresses (may be repeated). 
        cc          Carbon copy addresses (may be repeated). 
        bcc         Blind carbon copy addresses (may be repeated). 
        subject     Short description.
        text        Plain text body string.
        filename    Import plain text body from file (stdin if `-`).
        attach      MIMEText attachments.
    """

# if empty keyword argument, try loading from user config, then default
    kw = {'smtpserver':'sendemail.smtpserver',
            'name':'user.name',
            'email':'user.email',
            'to':'sendemail.to',
            'cc':'sendemail.cc',
            'bcc':'sendemail.bcc'}
    default = {'smtpserver':'localhost',
            'name':'Nobody',
            'email':'nobody@no.where'}
    for aname, cname in kw.items():
        arg = eval(aname)
        if arg:
            kw[aname] = arg
        elif cname in self.config:
            kw[aname] = self.config[cname]
        elif aname in default:
            kw[aname] = default[aname]
        else:
            kw[aname] = None
    utcnow = datetime.utcnow()
    msg = MIMEMultipart(_subparts=attach) if attach else Message() 
    msg.set_unixfrom('From %s %s'
            % (email, utcnow.strftime("%a %b %d %H:%M:%S %Y")))
    msg.add_header('Date', utcnow.strftime("%a, %d %b %Y %H:%M:%S +0000"))
    if name:
        msg.add_header('From', '%s <%s>' % (kw['name'], kw['email']))
    if subject:
        msg.add_header('Subject', subject)
    recipients = []
    header = { 'to':'To', 'cc':'Cc' }
    for opt in 'to', 'cc', 'bcc':
        val = kw[opt]
        if val:
            for addr in val if isinstance(val,list) else [ val ]:
                try:
                    addr = self.config['sendemail.alias.%s' % addr]
                except KeyError:
                    pass
                if opt in header:
                    msg.add_header(header[opt], addr)
                recipients.append(addr)
    if text:
        msg.set_payload(text)
    if filename:
        f = sys.stdin if filename == '-' else open(filename, 'r')
        msg.set_payload(f.read())
    if dry_run:
        msg.add_header('X-From', kw['email'])
        msg.add_header('X-Recipients', ', '.join(recipients))
        pydoc.pager(str(msg))
    else:
        s = SMTP(kw['smtpserver'])
        nondelivery = s.sendmail(kw['email'], recipients, str(msg))
        for addr, reason in nondelivery.items():
            print("Not delivered to '%s', %s" % (addr, reason))
        s.quit()
