import sys
from config import *

def main():
    if len(sys.argv) < 2:
        print("Usage: oi command [arguments]")
        exit(1)
    cmd = sys.argv[1]
    if cmd not in COMMANDS:
        print("Supported commands: " + ", ".join(COMMANDS))
        exit(1)

    if len(sys.argv) == 2:
        COMMANDS[cmd]([])
    else:
        COMMANDS[cmd](sys.argv[2:])
