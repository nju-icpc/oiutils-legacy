#!/usr/bin/python

"""
This is a preliminary version used in JSOI
"""


import re, subprocess
from subprocess import PIPE

FILENAME = "README.pdf"

IPs = []
for line in open("IP_LIST", "r").read().strip().split("\n"):
    if re.match(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', line):
        IPs.append(line)
    else:
        print "[Error]: bad line ", line
        exit(1)

def execute(args):
    return subprocess.Popen(args, stdout=PIPE, stderr=PIPE)

SSH_OPTIONS = ["-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=10"]

def remote(ip, *cmd):
    return ["ssh", "-p", "2222"] + SSH_OPTIONS + [ip] + list(cmd)

def send(ip, fname):
    return ["scp", "-P", "2222"] + SSH_OPTIONS + [fname, "%s:/mnt/shared/" % ip]

procs = []
for ip in IPs:
#    cmd = remote(ip, 'true')
    cmd = send(ip, FILENAME)
    p = execute(cmd)
    procs.append(p)

for (ip, p) in zip(IPs, procs):
    (o1, o2) = p.communicate()
    print ip, 
    if p.returncode == 0:
        print "OK"
    else:
        print "ERROR"
        print o2
