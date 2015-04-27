import argparse, tempfile, os, shutil

COMPILERS = {
    'c': 'gcc',
    'cpp': 'g++',
    'pas': 'fpc',
}

# compile should generate "a.exe" on the same directory
def compile_cmd(options, src):
    ext = src.split('.')[-1]         # cpp
    opt = ' '.join(options)

    if ext == 'cpp':
        return 'g++ %s -o a.exe %s' % (opt, src)
    elif ext == 'c':
        return 'gcc %s -o a.exe %s' % (opt, src)
    elif ext == 'pas':
        return 'fpc %s -oa.exe %s' % (opt, src)
    else:
        return ''

def oi_compile(args):
    try:
        if len(args) == 0: args = ['-h']
        parser = argparse.ArgumentParser(description = 'compile a source file.')
        parser.add_argument('-o', help = 'output file', default = 'a.exe')
        parser.add_argument('file', help = 'source code file', nargs = 1)
        parser.add_argument('--optimized', help = 'using optimized compiling', default = False, action = "store_true")

        options = vars(parser.parse_args(args))
        opt = []
        if options['optimized']:
            opt.append('-O2')

        fname = options.get('file')[0]   # xyz/src/a.cpp
        dest = options.get('o')
        src = os.path.basename(fname)    # a.cpp
        tmpdir = tempfile.mkdtemp()      # /tmp/abc123

        shutil.copy(fname, tmpdir)
        
        print compile_cmd(opt, src)
        os.system('cd "%s" && %s' % (tmpdir, compile_cmd(opt, src)) )
        exe = os.path.join(tmpdir, 'a.exe')
        shutil.copy(exe, dest)
    except:
        pass
