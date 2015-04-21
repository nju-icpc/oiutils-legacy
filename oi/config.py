from contest.contest import oi_run_contest
from contest.texify import oi_texify_report

COMMANDS = {
    'sandbox': None,
    'judge': None,
    'run': oi_run_contest,
    'texify': oi_texify_report,
}
