from contest.contest import oi_run_contest
from contest.texify import oi_texify_report
from sandbox.sandbox import oi_sandbox

COMMANDS = {
    'sandbox': oi_sandbox,
    'judge': None,
    'run': oi_run_contest,
    'texify': oi_texify_report,
}
