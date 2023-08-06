"""Helper functions for making things readable by humans."""
import inspect
import types


__all__ = ['humanize_bytes', 'print_table']


def print_table(headers, columns, order=None):
    """Pretty-prints a table.

    Parameters:
        headers (list of str): The column names.
        columns (list of lists of str): The column values.
        order (list of ints): Order in which to print the column the values. Defaults to the order
            in which the values are given.

    """

    # Check inputs
    if len(headers) != len(columns):
        raise ValueError('there must be as many headers as columns')

    if len(set(map(len, columns))) > 1:
        raise ValueError('all the columns must be of the same length')

    # Determine the width of each column based on the maximum length of it's elements
    col_widths = [
        max(*map(len, col), len(header))
        for header, col in zip(headers, columns)
    ]

    # Make a template to print out rows one by one
    row_format = ' '.join(['{:' + str(width + 2) + 's}' for width in col_widths])

    # Determine the order in which to print the column values
    if order is None:
        order = range(len(columns[0]))

    # Build the table
    table = (
        row_format.format(*headers) + '\n' +
        '\n'.join((
            row_format.format(*[
                col[i].rjust(width)
                for col, width in zip(columns, col_widths)
            ])
            for i in order
        ))
    )

    return table


def humanize_bytes(n_bytes):
    """Returns a human-friendly byte size."""
    for unit in ('', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'):
        if abs(n_bytes) < 1024:
            return f'{n_bytes:3.1f}{unit}B'
        n_bytes /= 1024
    return f'{n_bytes:.1f}YiB'
