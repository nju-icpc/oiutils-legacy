#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, platform, os, subprocess, yaml, hashlib
from contest import *

def get_filesystem_encoding():
    if platform.system() == "Windows": 
        return 'gbk'
    else:
        return 'utf-8'

def get_processor_name():
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        command = ['sysctl', '-n', 'machdep.cpu.brand_string']
        return subprocess.check_output(command).strip()
    elif platform.system() == "Linux":
        command = ['cat', '/proc/cpuinfo']
        all_info = subprocess.check_output(command, shell=True).strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub( ".*model name.*:", "", line,1)
    return u"标准测试环境"

def oi_texify_report(args):
    PATH = '.'
    cst = unicode(args[0], get_filesystem_encoding())
    YAML_FILE = os.path.join(PATH, 'contest.yaml')
    PROGRAM_DIR = os.path.join('programs')

    data = [i for i in yaml.load_all(open(YAML_FILE, "r").read())]
    meta = data[0]
    problems = data[1:]
    Makefile = []

    def find_source(directory, prob):
        for fn in prob['allowed_file']:
            fname = os.path.join(PATH, PROGRAM_DIR, directory, fn)
            if os.path.isfile(fname):
                return os.path.join(PROGRAM_DIR, directory, fn)
        return None
    
    def get_contestants():
        ret = [i for i in os.listdir(unicode(os.path.join(PATH, PROGRAM_DIR))) if not i.startswith('.')]
        return ret

    def read_file(fn):
        with open(os.path.join(PATH, fn), "r") as fp:
            return fp.read().decode('utf-8')

    def write_file(fn, data):
        with open(os.path.join(PATH, fn), "w") as fp:
            fp.write(data.encode('utf-8'))

    TEX_HEADER = (
""" % !Mode:: "TeX:UTF-8"
\documentclass[10pt,a4paper]{article}
\usepackage{xltxtra,fontspec,xunicode}
\usepackage[slantfont,boldfont]{xeCJK} 
\usepackage{fancyhdr}
\pagestyle{fancy}
\lhead{}
\chead{}
\\rhead{}
\lfoot{}
\\rfoot{}%{\\thepage}
\setlength{\parindent}{0cm}
\setCJKmainfont{SimSun}""")

    Tex = [TEX_HEADER, '\\begin{document}']
    Tex.append('\\cfoot{--- {\\sf oiutils} and \XeTeX, %s ---}' % get_processor_name())
    Tex.append('\\rhead{%s}' % cst)
    Tex.append(u'\\section*{%s -- [选手：%s]}' % (meta['title'], cst))
    for prob in problems:
        prob_title = prob['name'] + ' (%s)' % prob['abbrv']
        fn = find_source(cst, prob)
        if fn is not None:
            log = compile_task(cst, prob)
            src_name = fn.split(os.path.sep)[-1]
            src = read_file(fn)
            md5 = hashlib.md5(src).hexdigest()[:6]
            
            executable = '.'.join(log.split('.')[:-1] + ['exe'])
            compiled = os.path.isfile(executable)
            Tex.append(u'\\subsection*{%s{\\normalsize\\dotfill\\tt %s (%s, %d字节)}}\n' % (prob_title, src_name, md5, len(src)))
            if compiled:
                for (ti, case) in enumerate(prob['testcases']):
                    test = test_task(cst, prob, ti)
                    Tex.append('Test Case \\# %d: ' % (ti+1))
                    Tex.append(
                    '%s\n'
                    % read_file(test_task(cst, prob, ti))[:10])
            else:
                Tex.append(u'编译错误。')
        else:
            Tex.append(u'\\subsection*{%s}' % prob_title)
            Tex.append(u'找不到文件。')

    Tex.append('\n\\vfill\n')
    Tex.append(u'\n选手签字 \\underline{\\vspace{4cm}} 教师签字\n')
    Tex.append(u'签字代表对评测结果确认无误。\n')
    Tex.append('\n\\vspace{1cm}\n')

    Tex.append('\\end{document}')
    write_file(os.path.join('report', cst + '.tex'), '\n'.join(Tex))
    
    subprocess.call(['bash', '-c', ('cd report && xelatex %s.tex < /dev/null &> /dev/null' % cst).encode(get_filesystem_encoding())])
    os.system("rm -f report/*.aux report/*.log")
