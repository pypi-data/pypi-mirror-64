import re
import sys
from pprint import pprint
from itertools import count
import plac
import textwrap
from . import mydecs
from . import version
import csv
from .utils import get_attr

def parse_genbank(stream):

    try:
        from Bio import SeqIO
    except ImportError as exc:
        print(f"*** {exc}")
        print(f"*** This software requires biopython.")
        print(f"*** Try: conda install biopython")
        sys.exit(1)

    recs = SeqIO.parse(stream, "genbank")

    return recs


def hr(sep="-", size=80):
    print(sep * size)


def wrap(text):
    return "\n".join(textwrap.wrap(text))


def print_data(stream, gb):

    # Parse the genbank stream.

    chroms = dict()
    rows = list(line.split() for line in stream)
    for row in rows:
        chroms.setdefault(row[0], []).append(row[1:])

    def match_chrom(rec):
        return rec.name in chroms

    recs = parse_genbank(gb)

    # We put it here to avoid adding a global dependency.
    from Bio.Seq import MutableSeq, Seq

    # Take only records that we have variations for.
    recs = filter(match_chrom, recs)

    def select_cds(feat):
        return feat.type == "CDS"

    for rec in recs:

        feats = filter(select_cds, rec.features)
        feats = list(feats)

        variations = chroms[rec.name]

        for pos, ref, alt in variations:

            loc = int(pos) - 1

            for feat in feats:
                start = int(feat.location.start)
                end = int(feat.location.end)

                if start <= loc < end:
                    #print(feat)
                    shift = loc - start
                    idx, frame = divmod(shift, 3)

                    c_start = idx * 3
                    c_end = c_start + 3

                    dna1 = feat.location.extract(rec).seq
                    dna2 = MutableSeq(str(dna1))
                    dna2[shift] = alt
                    dna2 = Seq(str(dna2))

                    codon1 = dna1[c_start: c_end]
                    codon2 = dna2[c_start: c_end]

                    prot1 = dna1.translate()
                    prot2 = dna2.translate()

                    feat_name = get_attr(feat, "gene")

                    p1, p2 = prot1[idx], prot2[idx]
                    symb = "syn" if p1 == p2 else "non"
                    data = [rec.name , feat_name, pos, f"{ref}/{alt}", frame+1, codon1, codon2, p1, p2, symb ]

                    data = map(str, data)

                    line  = "\t".join(data)

                    print (line)

import argparse

@plac.annotations(
    g=("Genbank file", "option", None, argparse.FileType('rt'), None, None),
)
def run(g):
    "Prints the effect of an annotation"

    stream = sys.stdin

    print_data(stream=stream, gb=g)

def main():
    plac.call(run)


if __name__ == '__main__':
    main()
