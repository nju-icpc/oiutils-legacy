# -*- coding: utf-8 -*-
import argparse, tempfile, shutil, os

def oi_receive(args):
    if len(args) == 0: args = ['-h']
    parser = argparse.ArgumentParser(description = 'send a file to a destination')
    parser.add_argument('-i', help = 'private key file')
    parser.add_argument('-p', help = 'port', default = '22')
    parser.add_argument('-timeout', help = 'time out (s)', default = '10')
    parser.add_argument('files', help = 'files to be send', nargs = argparse.REMAINDER)
    options = vars(parser.parse_args(args))

    key = options.get('i')
    port = options.get('p')
    timeout = options.get('timeout')
    args = options.get('files')

    print "To:", timeout, " Port:", port
    print "Key:", key
    print args

    # We need a ssh wrapper!

def oi_receive_gui():
    pass
