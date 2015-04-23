# -*- coding: utf-8 -*-
import argparse

def verdict(yes, msg):
    print msg
    if yes:
        print "1.0"
        exit(0)
    else:
        print "0.0"
        exit(1)

"""
Compares two files line-by-line, with head and trailing whitespaces stripped out
"""
def oi_fc(args):
    try:
        if len(args) == 0: args = ['-h']
        parser = argparse.ArgumentParser(description = 'compile a source file.')
        parser.add_argument('file1', help = 'the first file', nargs = 1)
        parser.add_argument('file2', help = 'the second file', nargs = 1)
        parser.add_argument('-s', help = 'the comparison script', default = '')
        
        options = vars(parser.parse_args(args))

        f1 = options.get('file1')[0]
        f2 = options.get('file2')[0]

        try:
            with open(f1, "r") as fp:
                L1 = fp.read()
            with open(f2, "r") as fp:
                L2 = fp.read()
        except:
            verdict(False, "无输出")

        lines1 = [l.strip() for l in L1.strip().split('\n')]
        lines2 = [l.strip() for l in L2.strip().split('\n')]

        if len(lines1) != len(lines2):
            verdict(False, "错误(行数不匹配)")

        for i in range(0, len(lines1)):
            if lines1[i] != lines2[i]:
                verdict(False, "错误(第%d行)" % (i + 1))
        exit(0)
    except Exception, e:
        print e
        verdict(False, "出错")
