#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, platform, os, subprocess, yaml, hashlib
from contest import *

def get_filesystem_encoding():
    if platform.system() == "Windows": 
        return 'gbk'
    else:
        return 'utf-8'

def get_system_info():
    if platform.system() == "Windows":
        return platform.system() + ' ' + platform.release()
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
\usepackage{multicol}
\pagestyle{fancy}
\lhead{}
\chead{}
\\rhead{}
\lfoot{}
\\rfoot{}%{\\thepage}
\setlength{\parindent}{0cm}
\setCJKmainfont{SimSun}""")

    Tex = [TEX_HEADER, '\\begin{document}']
    Tex.append('\\cfoot{--- {\\sf oiutils} and \XeTeX, %s ---}' % get_system_info())
    Tex.append('\\rhead{%s}' % cst)
    Tex.append(u'\\section*{%s -- [%s]}' % (meta['title'], cst))
    total_score = 0
    for prob in problems:
        prob_title = prob['name'] + ' (%s)' % prob['abbrv']
        fn = find_source(cst, prob)
        prob_score = 0
        if fn is not None:
            log = compile_task(cst, prob)
            src_name = fn.split(os.path.sep)[-1]
            src = read_file(fn)
            md5 = hashlib.md5(src).hexdigest()[:6]
            Tex.append(u'\\subsection*{%s{\\normalsize\\dotfill\\tt %s (%s, %d字节)}}\n' % (prob_title, src_name, md5, len(src)))
        Tex.append('\\begin{multicols}{2}')
        if fn is not None:
            executable = '.'.join(log.split('.')[:-1] + ['exe'])
            compiled = os.path.isfile(executable)
            if compiled:
                for (ti, case) in enumerate(prob['testcases']):
                    test = test_task(cst, prob, ti)
                    res = read_file(test_task(cst, prob, ti)).strip().split('\n')
                    case_score = prob['score']
                    if 'score' in case: case_score = case['score']
                    case_score = int(float(case_score) * float(res[-1]))
                    prob_score += case_score
                    Tex.append(u'测试点\\#%d: ' % (ti+1))
                    Tex.append(u'%s\\dotfill~%d分\n' % (res[-2], case_score))
                total_score += prob_score
            else:
                Tex.append(u'编译错误。')
        else:
            Tex.append(u'\\subsection*{%s}' % prob_title)
            Tex.append(u'找不到文件。')
        Tex.append('\\end{multicols}')
        Tex.append(u'\\hfill~本题得分： %d\n' % prob_score)

    Tex.append('\n\\vfill\n')
    Tex.append(u'{\Large \\hfill总分: %d}\n' % total_score)
    Tex.append(u'\\hfill\\begin{tabular}{r} \\vspace{1.5cm}\\hspace{4cm} \\\\ \\hline 选手确认签字\end{tabular}')
    Tex.append('\\hspace{1em}')
    Tex.append(u'\\begin{tabular}{r} \\vspace{1.5cm}\\hspace{4cm} \\\\ \\hline 指导教师确认签字\end{tabular}')
    Tex.append('\n\\vspace{0.3cm}')
    Tex.append(u'\\hfill签字即代表对此评测结果表示认可。')

    Tex.append('\\end{document}')
    write_file(os.path.join('report', cst + '.tex'), '\n'.join(Tex))
    
    subprocess.call(['bash', '-c', ('cd report && xelatex %s.tex < /dev/null &> /dev/null' % cst).encode(get_filesystem_encoding())])
    os.system("rm -f report/*.aux report/*.log")
