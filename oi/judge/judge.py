# -*- coding: utf-8 -*-
import argparse, tempfile, shutil, os

def verdict(yes, msg):
    print msg
    if yes:
        print "1.0"
        exit(0)
    else:
        print "0.0"
        exit(1)

def oi_judge(args):
    if len(args) == 0: args = ['-h']
    parser = argparse.ArgumentParser(description = 'judge a file with input and output')
    parser.add_argument('-tl', help = 'time limit (seconds)', default = '1')
    parser.add_argument('-ml', help = 'memory limit (megabytes)', default = '64')
    parser.add_argument('-I', help = 'input file path')
    parser.add_argument('-O', help = 'answer file path')
    parser.add_argument('-i', help = 'input file name (can be stdin)')
    parser.add_argument('-o', help = 'output file name (can be stdout)')
    parser.add_argument('execfile', help = 'the executable', nargs = 1)
    options = vars(parser.parse_args(args))

    execfile = options.get('execfile')[0]
    tl = options.get('tl')
    ml = options.get('ml')
    ifname = options.get('i')
    ofname = options.get('o')
    infile = options.get('I')
    ansfile = options.get('O')
    
    # copy useful files
    tmpdir = tempfile.mkdtemp()      # /tmp/abc123
    try:
        shutil.copy(execfile, os.path.join(tmpdir, 'a.exe'))
    except:
        verdict(False, "找不到可执行文件")

    try:
        shutil.copy(infile, os.path.join(tmpdir, ifname))
    except:
        verdict(False, "读取输入文件失败")

    ret = os.system('cd "%s" && %s' %  (tmpdir, 'oi sandbox -t "%s" -m "%s" ./a.exe' % (tl, ml)) )
    if ret != 0:
        exit(ret)

    O = os.path.join(tmpdir, ofname)
    A = ansfile
    
    if not os.path.isfile(O) or not os.path.isfile(A):
        verdict(False, "无输出")

    ret = os.system('oi fc "%s" "%s"' % (O, A))
    if ret != 0:
        verdict(False, "错误")
    verdict(True, "正确")
