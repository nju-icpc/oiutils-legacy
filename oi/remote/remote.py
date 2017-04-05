# -*- coding: utf-8 -*-
import argparse, tempfile, shutil, os, subprocess
from subprocess import PIPE

def execute(args):
    p = subprocess.Popen(args, stdout=PIPE, stderr=PIPE)
    (out, err) = p.communicate()
    return (p.returncode, out, err)

def remote_do(ip, *cmd):
    SSH_OPTIONS = ["-i", key, "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout={0}".format(timeout), "-p", port]
    args = ["ssh"] + SSH_OPTIONS + [ip] + list(cmd)
    return execute(args)

def remote_copy(ip, fname, dest):
    SSH_OPTIONS = ["-i", key, "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout={0}".format(timeout), "-P", port]
    args = ["scp"] + SSH_OPTIONS + [fname, "{0}:{1}".format(ip, dest)]
    return execute(args)

def oi_remote(args):
    global port, timeout, key
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

    (ret, out, err) = remote_do('jsoi-admin@localhost', 'ls -l /media/sf_shared')
    if ret == 0:
        print out
    else:
        print "ERROR"
        print err

# TODO:
# commands:
#   send DIR -> return DIRNAME
#   execute ls -l /media/sf_shared


# Scenarios:
#   1. upload a README.pdf
#   2. upload a problem.pdf
#   3. get files in the dir.

def oi_send_gui():
    pass
