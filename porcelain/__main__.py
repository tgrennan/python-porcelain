#! /usr/bin/python3.1

import sys
import collections
sys.path.insert(0, sys.path[0].replace('/porcelain',''))
from .__init__ import Porcelain, Options, __version__

args = sys.argv[1:]
opts = Options(args)

if 'version' in opts:
# python3 -m porcelain --version
    print(__version__)
    sys.exit(0)

if 'help' in opts:
    if opts['help'] == True:
# python3 -m porcelain --help
        help('porcelain')
    else:
        name_ = opts['help'].replace('-','_')
        try:
# python3 -m porcelain --help METHOD
            help(getattr(Porcelain(), name_))
        except AttributeError as e:
# python3 -m porcelain --help INVALID_METHOD
            sys.exit(e)
    sys.exit(0)

try:
    porcelain = Porcelain(**opts)
    name = args.pop(0)
    name_ = name.replace('-','_')
except TypeError as e:
    sys.exit('Porcelain.' + str(e))
except IndexError:
# python3 -m porcelain
    help('porcelain')
    sys.exit(0)

if name == 'help':
    try:
# python3 -m porcelain help METHOD
        name = args.pop(0)
        name_ = name.replace('-','_')
        help(getattr(porcelain, name_))
    except IndexError:
# python3 -m porcelain help
        help('porcelain.Porcelain')
    except AttributeError as e:
# python3 -m porcelain help INVALID_METHOD
        sys.exit(e)
    sys.exit(0)

if name == 'git':
    command = args.pop(0) if len(args) else None
    mopts = {'stdout': sys.stdout}
    sys.exit(getattr(porcelain, name)(command, *args, **mopts))

try:
    attr = getattr(porcelain, name_)
    mopts = Options(args)
    if 'help' in mopts:
# python3 -m porcelain METHOD --help
        args = [ name_ ]
        attr = help
    sys.exit(attr(*args, **mopts))
except AttributeError as e:
    sys.exit(str(e))
except TypeError:
# print attribute if not callable
    if len(args):
        if args[0] in attr:
            print(str(attr[args[0]]))
        else:
            sys.exit("No '%s' in '%s'." % (args[0], name))
    else:
        print(str(attr))
