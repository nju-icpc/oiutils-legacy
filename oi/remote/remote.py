# -*- coding: utf-8 -*-
import argparse, tempfile, shutil, os, subprocess
from subprocess import PIPE
from multiprocessing import Process

def execute(args):
    p = subprocess.Popen(args, stdout=PIPE, stderr=PIPE)
    (out, err) = p.communicate()
    return (p.returncode, out, err)

def remote_do(ip, cmd):
    SSH_OPTIONS = ["-i", key, "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout={0}".format(timeout), "-p", port]
    args = ["ssh"] + SSH_OPTIONS + [ip] + cmd
    return execute(args)

def remote_upload(ip, src, dest):
    SSH_OPTIONS = ["-i", key, "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout={0}".format(timeout), "-P", port]
    args = ["scp"] + SSH_OPTIONS + [src, "{0}:{1}".format(ip, dest)]
    return execute(args)

def remote_download(ip, src, dest):
    SSH_OPTIONS = ["-i", key, "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout={0}".format(timeout), "-P", port]
    args = ["scp"] + SSH_OPTIONS + ["{0}:{1}".format(ip, src)] + [dest]
    return execute(args)

def oi_remote(args):
    global port, timeout, key
    if len(args) == 0: args = ['-h']
    parser = argparse.ArgumentParser(description = 'send a file to a destination')
    parser.add_argument('-key', help = 'private key file')
    parser.add_argument('-port', help = 'port', default = '22')
    parser.add_argument('-timeout', help = 'time out (s)', default = '10')
    parser.add_argument('-host', help = 'host IP/name')
    parser.add_argument('command', help = 'the command to be executed', choices = {"execute", "upload", "download"}, nargs = 1)
    parser.add_argument('args', help = 'arguments', nargs = argparse.REMAINDER)
    options = vars(parser.parse_args(args))

    key = options.get('key')
    port = options.get('port')
    timeout = options.get('timeout')
    host = options.get('host')
    cmd = options.get('command')[0]
    args = options.get('args')

    # execute command
    # upload src(host) dest(remote)
    # download src(remote) dest(host)

    if cmd == 'execute':
        (ret, out, err) = remote_do('jsoi-admin@{0}'.format(host), args)
        if ret == 0: print out
        exit(ret)
    elif cmd == 'upload':
        (ret, out, err) = remote_upload('jsoi-admin@{0}'.format(host), args[0], args[1])
        if ret == 0: print out
        exit(ret)
    elif cmd == 'download':
        (ret, out, err) = remote_download('jsoi-admin@{0}'.format(host), args[0], args[1])
        if ret == 0: print out

def oi_send_gui():
    pass
