from typing import List

from libdiff.utils import sequence_compare


def get_lcs_length(base_seq: List[str], target_seq: List[str]) -> List:
    """
    Get two of sequence and Return Two Dimension List called LCS
    ref: https://en.wikipedia.org/wiki/Longest_common_subsequence_problem

    :param base_seq: base sequence
    :param target_seq: target sequence
    :return: LCS
    """
    base_side_size = len(base_seq)
    target_side_size = len(target_seq)
    max_side_size = max(base_side_size, target_side_size)

    lcs = [[0 for _ in range(max_side_size)] for _ in range(max_side_size)]

    for row_index in range(base_side_size):
        lcs = get_row(base_seq, target_seq, row_index, target_side_size, lcs)

    return lcs


def get_row(base_seq, target_seq, row_index, target_side_size, lcs) -> List:
    """
    Generate row of LCS

    :param base_seq: base sequence
    :param target_seq: target sequence
    :param row_index: number who represent index of this row
    :param target_side_size: column size
    :param lcs: LCS
    :return:
    """
    for cell_index in range(target_side_size):
        base_sub_seq = base_seq[row_index]
        target_sub_seq = target_seq[cell_index]

        if sequence_compare(base_sub_seq, target_sub_seq):
            value = lcs[row_index-1][cell_index-1] + 1
        else:
            value = max(lcs[row_index][cell_index-1], lcs[row_index-1][cell_index])

        lcs[row_index][cell_index] = value

    return lcs


def print_diff(lcs, base, target, base_index, target_index):
    """
    Get backtrack LCS and print diff by recursively

    :param lcs:
    :param base:
    :param target:
    :param base_index:
    :param target_index:
    :return:
    """
    if base_index >= 0 and target_index >= 0 and base[base_index] == target[target_index]:
        print_diff(lcs, base, target, base_index-1, target_index-1)

    elif target_index >= 0 and is_added(base_index, target_index, lcs):
        print_diff(lcs, base, target, base_index, target_index-1)
        print("> " + target[target_index])

    elif base_index >= 0 and is_deleted(base_index, target_index, lcs):
        print_diff(lcs, base, target, base_index-1, target_index)
        print("< " + base[base_index])


def is_added(base_index, target_index, lcs):
    return base_index == 0 or lcs[base_index][target_index - 1] >= lcs[base_index - 1][target_index]


def is_deleted(base_index, target_index, lcs):
    return target_index == 0 or lcs[base_index][target_index - 1] <= lcs[base_index - 1][target_index]
