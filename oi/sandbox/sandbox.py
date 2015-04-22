import argparse, subprocess, os, psutil, time, sys

def kill_tree(p):
    try:
        for child in p.children(recursive = True):
            child.terminate()
        p.terminate()
    except:
        pass

def oi_sandbox(args):
    if len(args) == 0: args = ['-h']
    parser = argparse.ArgumentParser(description = 'put an executable in sandbox run with limits.')
    parser.add_argument('-t', help = 'time limit in milliseconds', default = '1.0')
    parser.add_argument('-m', help = 'memory limit in megabytes', default = '128')
    parser.add_argument('args', help = 'command to be executed', nargs = argparse.REMAINDER)
    
    options = vars(parser.parse_args(args))
    time_limit = float(options.get('t'))
    memory_limit = float(options.get('m'))

    if (len(options.get('args')) == 0):
        parser.parse_args(['-h'])
        
    p = subprocess.Popen(options.get('args'), shell = False)
    proc = psutil.Process(p.pid)

    start_time = time.time()

    (memory_use, time_use) = (0.0, 0.0)

    while True:
        current_time = time.time()

        try:
            memory_use = max(memory_use, proc.memory_info().rss / 1024.0 / 1024.0)
            time_use = current_time - start_time
        except:
            break

        if time_use > time_limit or \
           memory_use > memory_limit or \
           proc.status() in [psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD]:
            break

        time.sleep(0.01)

    kill_tree(proc)

    if time_use > time_limit:
        print "Time limit exceeded"
    if memory_use > memory_limit:
        print "Memory limit exceeded"

    print "%.2fs, %.2fMB" % (time_use, memory_use)
