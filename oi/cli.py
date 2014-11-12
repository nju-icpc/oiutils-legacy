import sys
from config import *

def main():
    if len(sys.argv) < 2:
        print("Usage: oi command [arguments]")
        exit(1)
    if sys.argv[1] not in COMMANDS:
        print("Supported commands: " + ", ".join(COMMANDS))
