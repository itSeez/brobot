import argparse
from copy import deepcopy
from itertools import combinations

bar = 45
plates = [0, 2.5, 5, 10, 25, 35, 45]

parser = argparse.ArgumentParser(description=f'Compute the plates needed at each side \
    of a barbell to reach the given weights. All wights must be multiples of 5 and a \
    minimum of {bar}.')
parser.add_argument(dest='t1', type=int, help='First weight target.')
parser.add_argument(dest='t2', type=int, help='Second weight target.')

def main(t1: int, t2: int | None) -> None:
    if t1 < bar or t2 < bar:
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

def print_solution(s: tuple) -> None:
    """Print the solution and split the plates that are common from the plates that are
    unique to each set.

    Arguments: s: A tiplet with the cost estimate as the first element and the sets of
                  weights as the second and third elements.
    """
    a = s[1]
    b = s[2]
    m = '\nCommon plates:'
    def add_number(m, n):
        if isinstance(n, float):
            m += f' {n:.1f}'
        elif n == 0:
            pass
        else:
            m += f' {n}'
        return m
    to_print_a = count(a)
    to_print_b = count(b)
    for w in a:
        if w in b:
            other = to_print_b
            target = to_print_a
            if to_print_a[w] > to_print_b[w]:
                other = to_print_a
                target = to_print_b
            while target[w]:
                m = add_number(m, w)
                other[w] -= 1
                target[w] -= 1
    m += '\nFirst Set:    '
    for w in a:
        while to_print_a[w]:
            m = add_number(m, w)
            to_print_a[w] -= 1
    m += '\nSecond Set:   '
    for w in b:
        while to_print_b[w]:
            m = add_number(m, w)
            to_print_b[w] -= 1
    print(m)

if __name__ == '__main__':
    main()
