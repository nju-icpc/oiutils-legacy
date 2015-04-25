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
    'u' : lambda a:int(a),
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
    _FULL = False
    if script[0] == '!':
        _FULL = True
        script = script.lstrip('!')
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

    return [r[0 : center], r[center], r[center + 1 : rlen] ,_FULL]


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

def fscompare(a, b, s):
    if len(s) == 2:
        if a != b: verdict(False, "Mismatched")
    else:
        if not s[2](func_dict[s[0] ](a), func_dict[s[0] ](b) ) : verdict(False, "Mismatched")

def scompare(a, b, s):
    if s[3]:
        ta = [a]
        tb = [b]
    else:
        ta = a.split()
        tb = b.split()
    if (len(ta) != len(tb) ): verdict(False, "Token count mismathed.")

    lc = rc = 0
    for i in xrange(len(s[0]) ):
        lc += int(s[0][i][1])
    for i in xrange(len(s[2]) ):
        rc += int(s[2][i][1])
    if (lc + rc > len(ta) ) : verdict(False, "No enough tokens to match your script.")

    sa = 0
    for i in xrange(len(s[0]) ):
        for j in xrange(int(s[0][i][1]) ):
            fscompare(ta[sa + j], tb[sa + j], s[0][i])
        sa += int(s[0][i][1])

    for i in xrange(lc, len(ta) - rc):
        fscompare(ta[i], tb[i], s[1])

    sb = -1
    for i in xrange(len(s[2]) ):
        for j in xrange(int(s[2][i][1]) ):
            fscompare(ta[sb - j], tb[sb - j], s[2][i])
        sb -= int(s[2][i][1])

"""
Compares two files line-by-line, with head and trailing whitespaces stripped out
"""

def oi_fc(args):
    try:
        if len(args) == 0: args = ['-h']
        parser = argparse.ArgumentParser(description = 'compare files with comparison script')
        parser.add_argument('file1', help = 'the first file', nargs = 1)
        parser.add_argument('file2', help = 'the second file', nargs = 1)
        parser.add_argument('-s', help = 'the comparison script', default = '[s+]+')
        
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

        lines1 = [l.strip('\r') for l in L1.strip().split('\n')]
        lines2 = [l.strip('\r') for l in L2.strip().split('\n')]

        if len(lines1) != len(lines2):
            verdict(False, "Mismatched line numbers.")

        cscript = options.get('s')
        if cscript != '':
            s = interpretl(cscript)
            lc = rc = 0
            for i in xrange(len(s[0]) ):
                lc += int(s[0][i][1])
            for i in xrange(len(s[2]) ):
                rc += int(s[2][i][1])
            if (lc + rc > len(lines1) ) : verdict(False, "No enough lines to match your script.")

            sa = 0
            for i in xrange(len(s[0]) ):
                for j in xrange(int(s[0][i][1]) ):
                    scompare(lines1[sa + j], lines2[sa + j], s[0][i][0])
                sa += int(s[0][i][1])

            for i in xrange(lc, len(lines1) - rc):
                scompare(lines1[i], lines2[i], s[1][0])

            sb = -1
            for i in xrange(len(s[2]) ):
                for j in xrange(int(s[2][i][1]) ):
                    scompare(lines1[sb - j], lines2[sb - j], s[2][i][0])
                sb -= int(s[2][i][1])
        verdict(True, "Matched.")
    except Exception, e:
        print e
        verdict(False, "An error occurred, comparison interrupted.")
