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

func_dict = {
    'e' : lambda a:eval(a),
    's' : lambda a:str(a),
    'd' : lambda a:int(a),
    'f' : lambda a:float(a)
}


def checkout_curtoken(r, cur_token):
    cur_token[0] = cur_token[0].strip()
    cur_token[1] = cur_token[1].strip()
    cur_token[1] = cur_token[1] or '1'

    if cur_token[1] == '*':
        cur_token[1] = '+'
    if (cur_token[1] != '+' and not cur_token[1].isdigit() ):
        verdict(False, 'Bad comparison script ([%s]%s)' % (cur_token[0], cur_token[1]) )

    for i in xrange(2, len(cur_token) ):
        cur_token[i] = eval('lambda a, b:' + cur_token[i])

    r.append(cur_token)


def interprett(script):
    print "interpreting script", script
    ccount = 0
    r = []
    state = 'idle'
    cur_token = ['', '']

    for i in xrange(len(script) ):
        if script[i] == '{' :
            ccount += 1
            if (state == 'idle' or state == 'dicted') and ccount == 1:
                if cur_token[0] == '' : cur_token = ['s', '']
                cur_token.append('')
                state = 'infunction'
                continue

        elif script[i] == '}' :
            if ccount <= 0 : verdict(False, "Mismatched bracket in script.")
            ccount -= 1
            if ccount == 0:
                state = 'dicted'
                continue

        if (state == 'idle' or state == 'dicted') and script[i].isalpha() and func_dict[script[i] ]:
            if (i != 0) : checkout_curtoken(r, cur_token)
            cur_token = [script[i], '']
            state = 'dicted'
        elif state == 'infunction':
            cur_token[len(cur_token) - 1] += script[i]
        elif state == 'dicted':
            cur_token[1] += script[i]
        else :
            verdict(False, "Wrong script")

    if ccount != 0 : verdict(False, "Unclosed bracket in script.")
    checkout_curtoken(r, cur_token)

    rlen = len(r)
    center = rlen - 1
    for i in xrange(rlen):
        if r[i][1] == '+':
            center = i
    r[center][1] = '+'

    return [r[0 : center], r[center], r[center + 1 : rlen] ]


def checkout_curline(r, cur_line):
    cur_line[0] = cur_line[0].strip()
    cur_line[1] = cur_line[1].strip()
    cur_line[1] = cur_line[1] or '1'
    if cur_line[1] == '*':
        cur_line[1] = '+'
    if (cur_line[1] != '+' and not cur_line[1].isdigit() ):
        verdict(False, 'Bad comparison script ([%s]%s)' % (cur_line[0], cur_line[1]) )
    r.append(cur_line)

def interpretl(script):
    ccount = 0
    r = []
    state = 'idle'
    cur_line = ['', '']

    for i in xrange(len(script) ):
        if (script[i] == '['):
            ccount += 1
            if (state == 'idle' or state == 'descriptor') and ccount == 1 :
                if i != 0 : checkout_curline(r, cur_line)
                cur_line = ['', '']
                state = 'inline'
                continue
        elif (script[i] == ']'):
            if ccount <= 0 : verdict(False, "Mismatched bracket in script.")
            ccount -= 1
            if state == 'inline' and ccount == 0 :
                state = 'descriptor'
                continue

        if state == 'descriptor' and ccount == 0:
            cur_line[1] += script[i]
        elif state == 'inline':
            cur_line[0] += script[i]
        else :
            verdict(False, "Wrong script")


    if ccount != 0 : verdict(False, "Unclosed bracket in script.")
    checkout_curline(r, cur_line)

    rlen = len(r)
    center = rlen - 1
    for i in xrange(rlen):
        r[i][0] = interprett(r[i][0])
        if r[i][1] == '+':
            center = i
    r[center][1] = '+'

    return [r[0 : center], r[center], r[center + 1 : rlen] ]


"""
Compares two files line-by-line, with head and trailing whitespaces stripped out
"""

def oi_fc(args):
    try:
        if len(args) == 0: args = ['-h']
        parser = argparse.ArgumentParser(description = 'compare files with comparison script')
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
            verdict(False, "No Output")

        lines1 = [l.strip() for l in L1.strip().split('\n')]
        lines2 = [l.strip() for l in L2.strip().split('\n')]

        if len(lines1) != len(lines2):
            verdict(False, "Mismatched line numbers.")

        cscript = options.get('s')
        if cscript != '':
            line_s = interpretl(cscript)
            print line_s
            lc = rc = 0
            for i in xrange(len(line_s[0]) ):
                lc += int(line_s[0][i][1])
            for i in xrange(len(line_s[2]) ):
                rc += int(line_s[2][i][1])
            print lc, rc


        for i in range(0, len(lines1)):
            print '"' + lines1[i] + '" "' + lines2[i] + '"'
            if lines1[i] != lines2[i]:
                verdict(False, "Mismatch.")
        exit(0)
    except Exception, e:
        print e
        verdict(False, "An error occurred, comparison interrupted.")
