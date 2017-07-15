from __future__ import print_function

import subprocess as sp


def percentile(sequence, percent):
    if not sequence:
        return None

    values = sorted(sequence)

    if percent == 0:
        return values[0]

    pos = int(len(values) * percent) - 1

    return values[pos]


def secs(value):
    units = ['s ', 'ms', 'us', 'ns']

    if value == 0:
        return '  0.000ns'
    else:
        for unit in units:
            if value > 1:
                return '%7.3f' % value + unit
            else:
                value *= 1000


def run(*args):
    "Run command, print output, and return output."
    print('utils$', *args)
    result = sp.check_output(args)
    print(result)
    return result.strip()


def display(name, timings):
    cols = ('Action', 'Count', 'Miss', 'Median', 'P90', 'P99', 'Max', 'Total')
    template = ' '.join(['%9s'] * len(cols))

    print()
    print(' '.join(['=' * 9] * len(cols)))
    print('Timings for %s' % name)
    print('-'.join(['-' * 9] * len(cols)))
    print(template % cols)
    print(' '.join(['=' * 9] * len(cols)))

    len_total = sum_total = 0

    for action in ['get', 'set', 'delete']:
        values = timings[action]
        len_total += len(values)
        sum_total += sum(values)

        print(template % (
            action,
            len(values),
            len(timings.get(action + '-miss', [])),
            secs(percentile(values, 0.5)),
            secs(percentile(values, 0.9)),
            secs(percentile(values, 0.99)),
            secs(percentile(values, 1.0)),
            secs(sum(values)),
        ))

    totals = ('Total', len_total, '', '', '', '', '', secs(sum_total))
    print(template % totals)
    print(' '.join(['=' * 9] * len(cols)))
    print()
