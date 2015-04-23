import argparse, tempfile, shutil, os

def oi_judge(args):
    if len(args) == 0: args = ['-h']
    parser = argparse.ArgumentParser(description = 'judge a file with input and output')
    parser.add_argument('-I', help = 'input file path')
    parser.add_argument('-O', help = 'answer file path')
    parser.add_argument('-i', help = 'input file name (can be stdin)')
    parser.add_argument('-o', help = 'output file name (can be stdout)')
    parser.add_argument('execfile', help = 'the executable', nargs = 1)
    options = vars(parser.parse_args(args))

    execfile = options.get('execfile')[0]
    ifname = options.get('i')
    ofname = options.get('o')
    infile = options.get('I')
    ansfile = options.get('O')
    
    # copy useful files
    tmpdir = tempfile.mkdtemp()      # /tmp/abc123
    try:
        shutil.copy(execfile, os.path.join(tmpdir, 'a.exe'))
    except:
        print "Cannot find executable"
        return

    try:
        shutil.copy(infile, os.path.join(tmpdir, ifname))
    except:
        print "Cannot create input file"

    os.system('cd "%s" && %s' %  (tmpdir, 'oi sandbox ./a.exe') )

    O = os.path.join(tmpdir, ofname)
    A = ansfile
    
    if not os.path.isfile(O) or not os.path.isfile(A):
        print "No output"
        return

    os.system('oi fc "%s" "%s"' % (O, A))
