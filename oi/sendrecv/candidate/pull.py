#!/usr/bin/python

"""
This is a preliminary version used in JSOI
"""

import sys, os, re, subprocess
from subprocess import PIPE
from multiprocessing import Process

USER = "root"
STU_ROOT = "/mnt/shared"
STU_PATH = r'/(30[124]-[0-9][0-9])-([a-zA-Z]+)/'
PORT = "2222"
PROBLEM  =  ["light", "binary", "attack"]
SSH_OPTIONS = ["-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=10"]

#####################################################

FILES = []
for p in PROBLEM:
    for e in [".c", ".cpp", ".pas"]:
        FILES.append('/' + p + e)

def execute(args):
#    print ' '.join(args)
    return subprocess.Popen(args, stdout=PIPE, stderr=PIPE)

def remote(ip, *cmd):
    return ["ssh", "-p", "2222"] + SSH_OPTIONS + ["%s@%s" % (USER, ip)] + list(cmd)

def send(ip, fname):
    return ["scp", "-P", "2222"] + SSH_OPTIONS + [fname, "%s@%s:/mnt/shared/" % (USER, ip)]

def receive(ip, files, dest):
    flist = ""
    for f in files:
        flist += " \"%s\"" % f
    flist = flist[1:]
    return ["scp", "-P", "2222"] + SSH_OPTIONS + ["%s@%s:%s" % (USER, ip, flist), dest]

def path_filter(s):
    m = re.search(STU_PATH, s.lower().replace(" ", "")) 
    if m is None: return (None, None)
    return (m.group(1), m.group(2))

def mkdir(path):
    try:
        os.mkdir(path)
    except:
        pass

def fetch(ip): 
    cmd = remote(ip, "find", STU_ROOT)
    p = execute(cmd)
    (oup, err) = p.communicate()
    if p.returncode != 0:
        print ip, "ERROR: no source found"
        return

    files = []
    
    submissions = set()
    for line in oup.strip().split('\n'):
        if True in [line.endswith(e) for e in FILES]:
            (seat, id) = path_filter(line)
            if seat and id:
                submissions.add( (seat, id) )
                files.append(line)

    if len(submissions) >= 1:
        (seat, id) = min(submissions)
        
        fname = "archive/%s-%s-%s" % (seat, id, ip)
        mkdir(fname)

        f = files[0]
        src = f.split('/')[-1]
        prob = src.split('.')[0]
        probdir = fname + '/'
        p = execute(receive(ip, files, probdir + '/'))
        (out, err) = p.communicate()
        if p.returncode != 0:
            print ip, "ERROR: copy failed"
        else:
            got = [i.split('/')[-1] for i in os.listdir(probdir + '/')]
            print ip, "OK", "%s-%s" % (seat, id), "[%s]" % (','.join(got))
    else:
        print ip, "ERROR: invalid submission"


mkdir('archive')
IPs = []
for line in open("IP_LIST", "r").read().strip().split("\n"):
    if line.startswith('#'): continue
    if re.match(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', line):
        IPs.append(line)
    else:
        print "[Error]: bad line ", line
        exit(1)

procs = [ Process(target = fetch, args = (ip, )) for ip in IPs ]

for p in procs: p.start()

for p in procs:
    p.join()

