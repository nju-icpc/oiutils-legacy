#!/usr/bin/python
import os, yaml, platform
from contest import *

"""
Takes one argument: the contest's directory path
"""
def oi_contest_run(args):
    PATH = args[0]
    YAML_FILE = os.path.join(PATH, 'contest.yaml')
    PROGRAM_DIR = path_join('programs')


    data = [i for i in yaml.load_all(open(YAML_FILE, "r").read())]
    meta = data[0]
    problems = data[1:]
    Makefile = []

    def find_source(directory, prob):
        for fn in prob['allowed_file']:
            fname = os.path.join(PATH, PROGRAM_DIR, directory, fn)
            if os.path.isfile(fname):
                return path_join(PROGRAM_DIR, directory, fn)
        return None
     
    def get_contestants():
        ret = [i for i in os.listdir(unicode(os.path.join(PATH, PROGRAM_DIR))) if not i.startswith('.')]
        return ret

    def gen_dep(task, dep_list, todo_list, phony = False):
        if phony:
            Makefile.append(".PHONY: " + task)
        Makefile.append(task + ': ' + ' '.join(dep_list))
        for item in todo_list:
            Makefile.append('\t' + item)
        Makefile.append("")

    def read_file(fn):
        with open(os.path.join(PATH, fn), "r") as fp:
            return fp.read().decode('utf-8')

    def write_file(fn, data):
        with open(os.path.join(PATH, fn), "w") as fp:
            fp.write(data.encode('utf-8'))

    gen_dep('all', ['init', 'compile', 'test', 'report', 'ranklist.csv'], [])
    all_logs = []
    all_tests = []

    for cst in get_contestants():
        for prob in problems:
            fn = find_source(cst, prob)
            if fn is not None:
                log = compile_task(cst, prob)
                all_logs.append(log)
                gen_dep(log, [fn], [
                    '-oi compile $< -o $(@:.log=.exe) &> $@' # do compile here
                ])
                for (ti, case) in enumerate(prob['testcases']):
                    test = test_task(cst, prob, ti)
                    all_tests.append(test)
                    ifn = path_join(prob['path'], case['input'])
                    ofn = path_join(prob['path'], case['output'])
                    tl = "1.0"
                    ml = "64"
                    tl = prob.get('time_limit', tl)
                    ml = prob.get('memory_limit', ml)
                    tl = case.get('time_limit', tl)
                    ml = case.get('memory_limit', ml)
                     
                    if 'fc_script' in prob:
                        fcs = '-fcs "%s"' % prob['fc_script'] + ' '
                    else:
                        fcs = ''
                
                    if 'spj' in prob:
                        spj = '-spj ' + prob['spj'] + ' '
                    else:
                        spj = ''
                    
                    gen_dep(test, [compile_task(cst, prob), ifn, ofn], [
                        '-oi judge -tl "%s" -ml "%s" -i "%s" -o "%s" -I "%s" -O "%s" %s "%s" &> $@'
                            % (tl, ml,
                               prob['input'], prob['output'],
                               ifn, ofn,
                               fcs + spj,
                               compile_exec(cst, prob)
                                ),
                    ])

    all_reports = []
    for cst in get_contestants():
        report_dep = []
        for prob in problems:
            fn = find_source(cst, prob)
            if fn is not None:
                report_dep.append( compile_task(cst, prob) )
                for (ti, case) in enumerate(prob['testcases']):
                    report_dep.append( test_task(cst, prob, ti) )
        rep = report_task(cst)
        gen_dep(rep, report_dep, [
            'oi contest-texify "%s" -o $@' % cst # generate report
        ])
        all_reports.append(rep)
                
    gen_dep('init', [], [
        '-@mkdir -p compiled tested report',
        '@echo === Compilation started ===',
    ], phony = True)
    gen_dep('compile', ['init'] + all_logs, [
        '@echo === Testing started ===',
    ], phony = True)
    gen_dep('test', ['compile'] + all_tests, [
        '@echo === Report generation started ===',
    ], phony = True)
    gen_dep('ranklist.csv', ['test'] + all_tests, [
        'oi contest-ranklist'
    ], phony = False)
    gen_dep('report', ['test'] + all_reports, [], phony = True)
    gen_dep('clean', [], ['rm -rf tested compiled report ranklist.csv'], phony = True)

    write_file("Makefile", '\n'.join(Makefile))

    os.system("cd \"%s\" && make" % PATH)
