import argparse
from copy import deepcopy
from itertools import combinations

bar = 45
plates = [0, 2.5, 5, 10, 25, 35, 45]

parser = argparse.ArgumentParser(add_help=False, description=f'Compute the plates needed at each side \
    of a barbell to reach the given weights. All weights must be multiples of 5 and a \
    minimum of {bar}.')
parser.add_argument(dest='t1', type=int, help='First weight target.')
parser.add_argument(dest='t2', type=int, help='Second weight target.')

def main(t1: int, t2: int) -> None:
    if t1 < bar or t2 < bar or t1 % 5 != 0 or t2 % 5 != 0:
        parser.print_help()
        return

    t1 = (t1 - bar) / 2
    t2 = (t2 - bar) / 2

    first_set = []
    second_set = []
    for i in range(1, len(plates)):
        for c in combinations(plates, i):
            w = sum(c)
            if w == t1:
                first_set.append(c)
            if w == t2:
                second_set.append(c)

    if len(first_set) == 0 or len(second_set) == 0:
        print('Unable to reach weight combination with the known plates.')
        return

    costs = []
    for fs in first_set:
        for ss in second_set:
            c = cost(fs, ss)
            l = len(fs) + len(ss)
            costs.append((c * l, fs, ss))

    costs.sort()
    print_solution(costs[0])

def count(a: tuple) -> dict:
    """Count the number of weights found in the given set.

    Argument: a: Set of weights.

    Return: Dictionary with weights as keys and their counts as values.
    """
    la = {}
    for w in a:
        la[w] = a.count(w)
    return la

def cost(a: tuple, b: tuple) -> int:
    """Estimate the cost of switching between the given sets of weights by adding the
    number of plates that is not common to either set.

    Arguments: a: First set of weights.
               b: Second set of weights.

    Return: Cost of the given weight combination.
    """
    la = count(a)
    lb = count(b)
    c = 0
    for a in deepcopy(la):
        for b in deepcopy(lb):
            if a == b:
                c += abs(la[a] - lb[b])
                del la[a]
                del lb[b]
    for a in la:
        c += la[a]
    for b in lb:
        c += lb[b]
    return c

def minimize_plates(group: tuple) -> tuple:
    """Replace a group with fewer known plates while preserving its total weight."""
    target = sum(group)
    available = [plate for plate in plates if plate > 0]
    for size in range(len(group)):
        for candidate in combinations(available, size):
            if sum(candidate) == target:
                return candidate
    return group

def print_solution(s: tuple) -> None:
    """Print the solution and split the plates that are common from the plates that are
    unique to each set.

    Arguments: s: A tiplet with the cost estimate as the first element and the sets of
                  weights as the second and third elements.
    """
    first = list(s[1])
    second = list(s[2])
    common = []
    for plate in s[1]:
        if plate in second:
            common.append(plate)
            first.remove(plate)
            second.remove(plate)

    lines = []
    for label, group in (
        ('Common plates:', common),
        ('First Set:    ', first),
        ('Second Set:   ', second),
    ):
        optimized = minimize_plates(tuple(group))
        values = ''.join(f' {plate:g}' for plate in sorted(optimized, reverse=True) if plate)
        lines.append(label + values)
    print('\n' + '\n'.join(lines))

if __name__ == '__main__':
    args = argparse.ArgumentParser(parents=[parser]).parse_args()
    main(args.t1, args.t2)
