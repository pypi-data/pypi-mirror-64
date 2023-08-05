# -*- coding: utf-8 -*-
"""Command line function."""
import sys
import click

from paczekfiller.paczekfiller import main_function as fry


def write(filename, contents):
    with open(filename, 'w') as file:
        file.write(contents)


@click.command()
@click.argument('paczek')
@click.argument('output_file')
def main(output_file, paczek):
    """Console script for Pączek filler."""

    try:
        write(output_file, fry(paczek))
        sys.exit(0)

    except EOFError:
        sys.stderr.write("Error EOF")
    except OSError:
        sys.stderr.write("Error loading template file. Is it really there?")
    except Exception as e:
        sys.stderr.write("Unexptected exception %s" % e)

    sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
