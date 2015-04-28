#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, platform, os, subprocess, yaml, hashlib
from contest import *

def oi_contest_ranklist(args):
    contest = Contest(".")

    Ranklist = []
    row = [u'选手'] + [prob['abbrv'] for prob in contest.problems] + [u'总分']
    Ranklist.append(row)
    for cst in contest.contestants:
        row = [cst]
        total_score = 0
        for prob in contest.problems:
            prob_score = 0
            if contest.find_source(cst, prob) is not None:
                if contest.find_executable(cst, prob) is not None:
                    for (ti, case) in enumerate(prob['testcases']):
                        test = test_task(cst, prob, ti)
                        res = contest.read_file(test_task(cst, prob, ti)).strip().split('\n')
                        case_score = prob['score']
                        if 'score' in case: case_score = case['score']
                        case_score = int(float(case_score) * float(res[-1]))
                        prob_score += case_score
                    total_score += prob_score
            row.append(str(int(prob_score)))
        row.append(str(int(total_score)))
        Ranklist.append(row)

    contest.write_file('ranklist.csv', '\n'.join([','.join(row) for row in Ranklist]))
