from contest.contest import oi_run_contest
from contest.texify import oi_texify_report

def sandbox(args):
    from sandbox.sandbox import oi_sandbox
    oi_sandbox(args)

COMMANDS = {
    'sandbox': lambda x: sandbox(x),
    'judge': None,
    'run': oi_run_contest,
    'texify': oi_texify_report,
}
