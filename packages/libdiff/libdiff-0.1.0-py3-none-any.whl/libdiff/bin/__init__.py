from libdiff.api import show_diff


def diff_bin(base, target):
    with open(base, "r") as f:
        base_file_line = f.readlines()

    with open(target, "r") as f:
        target_file_line = f.readlines()

    show_diff(base_file_line, target_file_line)
