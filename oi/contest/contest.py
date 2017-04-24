#!/usr/bin/python
import os, yaml, platform

def get_filesystem_encoding():
    if platform.system() == "Windows": 
        return 'gbk'
    else:
        return 'utf-8'

def compile_task(cst, prob):
    return path_join('compiled', '%s_%s.log' % (cst, prob['abbrv']))

def compile_exec(cst, prob):
    return path_join('compiled', '%s_%s.exe' % (cst, prob['abbrv']))

def test_task(cst, prob, tid):
    return path_join('tested', '%s_%s_%s.log' % (cst, prob['abbrv'], str(tid)))

def report_task(cst):
    return path_join('report', '%s.pdf' % cst)

def summary_task(cst):
    return path_join('tested', '%s_summary.log' % (cst))

def path_join(*args):
    return '/'.join(args)

class Contest:
    def __init__(self, path):
        self.path = path
        self.yaml_file = os.path.join(self.path, 'contest.yaml')
        self.program_dir = 'programs'

        self.data = [i for i in yaml.load_all(open(self.yaml_file, "r").read())]
        self.meta = self.data[0]
        self.problems = self.data[1:]
        self.contestants = [i for i in os.listdir(unicode(os.path.join(self.path, self.program_dir))) \
            if not i.startswith('.')]

    def read_file(self, fn):
        with open(os.path.join(self.path, fn), "r") as fp:
            return fp.read().decode('utf-8')

    def read_file_raw(self, fn):
        with open(os.path.join(self.path, fn), "r") as fp:
            return fp.read()

    def write_file(self, fn, data):
        with open(os.path.join(self.path, fn), "w") as fp:
            fp.write(data.encode('utf-8'))

    def find_source(self, cst, prob):
        for fn in prob['allowed_file']:
            fname = os.path.join(self.path, self.program_dir, cst, fn)
            if os.path.isfile(fname):
                return path_join(self.program_dir, cst, fn)
        return None

    def find_executable(self, cst, prob):
        log = compile_task(cst, prob)
        executable = '.'.join(log.split('.')[:-1] + ['exe'])
        if os.path.isfile(executable):
            return executable
        else:
            return None
        
