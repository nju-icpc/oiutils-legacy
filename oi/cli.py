import sys
from oiutils import *

def print_usage():
    print(
"""Usage: oi command [arguments]
Supported commands: """ + ', '.join(sorted([k for k in COMMANDS]))
)
    exit(1)

def main():
    if len(sys.argv) < 2: print_usage()

    cmd = sys.argv[1]
    if cmd not in COMMANDS: print_usage()

    f = ['oi'] + COMMANDS[cmd].split('.')

    mod = __import__('.'.join(f[:-1]), fromlist=[''])
    func = mod.__dict__[f[-1]]

    args = sys.argv[2:]
    func(args)
