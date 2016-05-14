# -*- coding: utf-8 -*-
import argparse, subprocess, os, psutil, time, sys

def oi_sched(args):
    if len(args) == 0: args = ['-h']
    parser = argparse.ArgumentParser(description = 'Scheduling a contest')
    parser.add_argument('args', help = 'layout files', nargs = argparse.REMAINDER)
    

    options = vars(parser.parse_args(args))

    if (len(options.get('args')) == 0):
        parser.parse_args(['-h'])
        
    # open a web-view to do the things

    exit(0)
