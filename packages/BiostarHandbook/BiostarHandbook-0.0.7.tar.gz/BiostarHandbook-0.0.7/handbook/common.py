import argparse
import csv
import itertools

import plac

FILL_VALUE = ''


def process(file1, file2, delimiter, colidx, show):
    """
    Processes the files and prints the output
    """

    def parse(stream):
        """
        A generator in a clojure to processes each stream.
        Returns the value of a column at the column index.
        """
        # Skip comment lines
        stream = filter(lambda x: not x.startswith('#'), stream)

        # Ignore empty lines.
        stream = filter(lambda x: x.strip(), stream)

        # Format the stream.
        stream = csv.reader(stream, delimiter=delimiter)

        # Generate empty values on missing columns.
        for row in stream:
            try:
                yield (row[colidx], None)
            except IndexError as exc:
                yield ('', None)

    # Make dictionaries to maintain original item order.
    store1 = dict(parse(file1))
    store2 = dict(parse(file2))

    # Generate the various groupings.
    isect = [key for key in store1.keys() if key in store2]
    onlyA = [key for key in store1.keys() if key not in store2]
    onlyB = [key for key in store2.keys() if key not in store1]
    union = isect + onlyA + onlyB
    # Select output based on flags.
    if show == 1:
        output = onlyA
    elif show == 2:
        output = onlyB
    elif show == 3:
        output = isect
    elif show == 4:
        output = union
    else:
        output = itertools.zip_longest(onlyA, onlyB, isect, union, fillvalue=FILL_VALUE)
        output = map(lambda x: "\t".join(x), output)

    # Print the output
    for line in output:
        print(line)


@plac.annotations(
    file1=("file 1", "positional", None, argparse.FileType('rt')),
    file2=("file 2", "positional", None, argparse.FileType('rt')),
    all=("show all columns", "flag", "a"),
    uniq1=("elements unique to file 1", "flag", "1"),
    uniq2=("elements unique to file 2", "flag", "2"),
    intersect=("elements in file 1 AND file 2", "flag", "i"),
    union=("elements in file 1 OR file 2", "flag", "u"),
    t=("tab delimited file (default CVS)", "flag"),
    c=("column index for values (default 1", "option"),
)

def run(file1, file2,  uniq1=False, uniq2=False, intersect=False, union=False, all=False, t=False, c=1):
    "A better 'comm' command to find common values."
    delimiter = "\t" if t else ","

    colidx = c - 1

    show = 0


    show = 1 if uniq1 else show
    show = 2 if uniq2 else show
    show = 3 if intersect else show
    show = 4 if union else show
    show = 0 if all else show

    process(file1=file1, file2=file2, delimiter=delimiter, colidx=colidx, show=show)


def main():
    """
    Entry point for the script.
    """

    plac.call(run)


if __name__ == '__main__':
    main()
