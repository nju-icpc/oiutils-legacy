import argparse, tempfile, os, shutil

COMPILERS = {
    'c': 'gcc',
    'cpp': 'g++',
    'pas': 'fpc',
}

# compile should generate "a.exe" on the same directory
def compile_cmd(src):
    ext = src.split('.')[-1]         # cpp
    if ext == 'cpp':
        return 'g++ "%s" -o a.exe' % src
    elif ext == 'c':
        return 'gcc "%s" -o a.exe' % src
    elif ext == 'pas':
        return 'fpc "%s"' % src
    else:
        return ''

def oi_compile(args):
    try:
        if len(args) == 0: args = ['-h']
        parser = argparse.ArgumentParser(description = 'compile a source file.')
        parser.add_argument('-o', help = 'output file', default = 'a.exe')
        parser.add_argument('file', help = 'source code file', nargs = 1)
        
        options = vars(parser.parse_args(args))

        fname = options.get('file')[0]   # xyz/src/a.cpp
        dest = options.get('o')
        src = os.path.basename(fname)    # a.cpp
        tmpdir = tempfile.mkdtemp()      # /tmp/abc123

        shutil.copy(fname, tmpdir)
        
        os.system('cd "%s" && %s' % (tmpdir, compile_cmd(src)) )
        exe = os.path.join(tmpdir, 'a.exe')
        shutil.copy(exe, dest)
    except:
        pass
