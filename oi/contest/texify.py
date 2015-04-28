#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, platform, os, subprocess, yaml, hashlib
from contest import *

def oi_contest_texify(args):
    contest = Contest(".")
    cst_raw = args[0]
    cst = unicode(args[0], get_filesystem_encoding())

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
\\cfoot{}
\\rfoot{}%{\\thepage}
\setlength{\parindent}{0cm}
\setCJKmainfont{SimSun}""")

    Tex = [TEX_HEADER, '\\begin{document}']
    Tex.append('\\lhead{%s}' % contest.meta['title'])
    Tex.append('\\rhead{%s}' % cst)
    Tex.append(u'\\section*{%s -- %s}' % (contest.meta['title'], cst))
    total_score = 0
    for prob in contest.problems:
        prob_title = prob['name'] + ' (%s)' % prob['abbrv']
        fn = contest.find_source(cst, prob)
        prob_score = 0
        if fn is not None:
            log = compile_task(cst, prob)
            src_name = fn.split(os.path.sep)[-1]
            src = contest.read_file_raw(fn)
            md5 = hashlib.md5(src).hexdigest()[:6]
            Tex.append(u'\\subsection*{%s{\\normalsize~\\dotfill~\\tt %s (%s, %d字节)}}\n' % (prob_title, src_name, md5, len(src)))
        Tex.append('\\begin{multicols}{2}')
        if fn is not None:
            executable = '.'.join(log.split('.')[:-1] + ['exe'])
            compiled = os.path.isfile(executable)
            if contest.find_executable(cst, prob) is not None:
                for (ti, case) in enumerate(prob['testcases']):
                    test = test_task(cst, prob, ti)
                    res = contest.read_file(test_task(cst, prob, ti)).strip().split('\n')
                    case_score = prob['score']
                    if 'score' in case: case_score = case['score']
                    case_score = int(float(case_score) * float(res[-1]))
                    prob_score += case_score
                    Tex.append(u'测试点\\#%d: ' % (ti+1))
                    Tex.append(u'%s~\\dotfill~%d分\n' % (res[-2], case_score))
                total_score += prob_score
            else:
                Tex.append(u'编译错误。')
        else:
            Tex.append(u'\\subsection*{%s}' % prob_title)
            Tex.append(u'找不到文件。')
        Tex.append('\\end{multicols}')
        Tex.append(u'\\hfill~本题得分： %d\n\\vfill' % prob_score)

    Tex.append('\n\\vfill\n')
    Tex.append(u'{\Large \\hfill 总分: %d}\n' % total_score)
    Tex.append(u'\\hfill\\begin{tabular}{r} \\vspace{1.5cm}\\hspace{4cm} \\\\ \\hline 选手确认签字\end{tabular}')
    Tex.append('\\hspace{1em}')
    Tex.append(u'\\begin{tabular}{r} \\vspace{1.5cm}\\hspace{4cm} \\\\ \\hline 指导教师确认签字\end{tabular}')

    Tex.append('\\end{document}')
    contest.write_file(os.path.join('report', cst + '.tex'), '\n'.join(Tex))
    
    cmd = 'xelatex "%s.tex" < /dev/null &> /dev/null' % cst
    cmd = cmd.encode(get_filesystem_encoding())

    subprocess.call(['bash', '-c', ('cd report && %s' % cmd)])
    os.system("rm -f report/*.aux report/*.log")
