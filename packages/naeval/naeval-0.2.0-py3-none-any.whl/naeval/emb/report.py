
import pandas as pd

from naeval.report import table_html


def format_mb(bytes):
    mb = bytes / 1024 / 1024
    return '%0.1f' % mb


def format_sec(secs):
    return '%0.1f' % secs


def format_mks(secs):
    mks = secs * 1000000
    return '%0.1f' % mks


def format_vocab(value):
    assert value < 1000000
    # 250001 -> 250K
    return '%dK' % int(value / 1000)


def report_table(scores, stats, datasets, schemes):
    data = []
    for scheme in schemes:
        bench = stats[scheme.name]
        row = [
            scheme.name,
            scheme.type,
            bench.init.value,
            bench.get.value,
            bench.disk,
            bench.ram,
            bench.vocab
        ]
        for dataset in datasets:
            score = scores[scheme.name, dataset]
            cover = score.count / score.total
            row.append([score.value, cover])
        data.append(row)

    columns = (
        ['model', 'type', 'init', 'get', 'disk', 'ram', 'vocab']
        + list(datasets)
    )
    table = pd.DataFrame(data, columns=columns)

    table = table.set_index('model')
    table.index.name = None  # no extra row in html

    return table


def format_cell(cell):
    score, cover = cell
    return '%0.3f/%0.2f' % (score, cover)


def format_github_cell(cell):
    score, cover = cell
    return '%0.3f' % score


def highlight(column, selection, format):
    for value in column:
        select = value in selection
        value = format(value)
        if select:
            value = '<b>%s</b>' % value
        yield value


def select_max(values, count=3, key=None):
    return sorted(values, key=key)[-count:]


def select_min(values, count=3, key=None):
    return sorted(values, key=key)[:count]


def first(pair):
    return pair[0]


def format_report(table, datasets):
    output = pd.DataFrame()
    output['type'] = table['type']

    columns = [
        ['init', format_sec, 'init, s'],
        ['get', format_mks, 'get, µs'],
        ['disk', format_mb, 'disk, mb'],
        ['ram', format_mb, 'ram, mb'],
    ]
    for column, format, name in columns:
        output[name] = table[column].map(format)

    for dataset in datasets:
        output[dataset] = table[dataset].map(format_cell)

    return table_html(output)


def format_github_report1(table):
    output = pd.DataFrame()
    output['type'] = table['type']

    columns = [
        ['init', format_sec, select_min, 'init, s'],
        ['get', format_mks, select_min, 'get, µs'],
        ['disk', format_mb, select_min, 'disk, mb'],
        ['ram', format_mb, select_min, 'ram, mb'],
        ['vocab', format_vocab, select_max, 'vocab']
    ]
    for column, format, select, name in columns:
        values = table[column].values
        selection = select(values)
        values = highlight(values, selection, format)
        output[name] = list(values)

    return table_html(output)


def format_github_report2(table, datasets):
    output = pd.DataFrame()
    output['type'] = table['type']

    for dataset in datasets:
        values = table[dataset].values
        selection = select_max(values, key=first)
        values = highlight(values, selection, format_github_cell)
        output[dataset] = list(values)

    output = output.rename(columns={'simlex965': 'simlex'})
    return table_html(output)
