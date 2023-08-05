"""
Various common utilities
"""
from itertools import zip_longest, count
from pprint import pprint


def flat_value(value, sep="|"):
    """
    Flattens values that may be lists.
    """
    if isinstance(value, list):
        return sep.join(value)
    else:
        return str(value)


def get_attr(feat, name):
    """
    Gets an attribute of a record.
    """
    if isinstance(feat, dict):
        value = feat.get(name)
    elif hasattr(feat, name):
        value = getattr(feat, name)
    elif hasattr(feat, "qualifiers"):
        value = feat.qualifiers.get(name, '')
    else:
        value = ''

    return flat_value(value or '')


def dna2prot(gx, loc=[]):
    """
    Computes the protein coordinate based on a genomic coordinate and potentially overlapping locations.
    gx: zero based genomic coordinate
    loc: a list of (start, end) pairs
    """
    # More than one protein may overlap with a genomic index due to negative frameshift.
    nt = 0
    ns = ''
    px = []
    for start, end in loc:
        # Both positions must be zero based
        if start <= gx < end:
            # The DNA lengths up to the genomic coordinate.
            nt = nt + (gx - start)
            div, mod = divmod(nt, 3)
            px.append((gx, nt, div, mod))
        else:
            # Sums the DNA lengths
            nt += end - start

    return px


def test():
    x = 48

    loc = [
        (10, 20),
        (30, 50),
        (45, 60),
    ]

    out = dna2prot(gx=x, loc=loc)

    print(out)


if __name__ == '__main__':
    test()
