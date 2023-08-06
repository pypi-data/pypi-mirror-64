from libdiff.core import get_lcs_length
from libdiff.core.core import print_diff


def show_diff(base, target):
    lcs = get_lcs_length(base, target)
    print_diff(lcs, base, target, len(base) - 1, len(target) - 1)
