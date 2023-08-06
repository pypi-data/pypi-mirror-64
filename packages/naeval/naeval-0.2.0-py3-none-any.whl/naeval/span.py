
from collections import defaultdict

from intervaltree import IntervalTree as Intervals

from naeval.record import Record


class Span(Record):
    __attributes__ = ['start', 'stop', 'type']
    __annotations__ = {
        'start': int,
        'stop': int
    }

    def __init__(self, start, stop, type=None):
        self.start = start
        self.stop = stop
        self.type = type

    def offset(self, delta):
        return Span(
            self.start + delta,
            self.stop + delta,
            self.type
        )


def offset_spans(spans, delta):
    for span in spans:
        yield span.offset(delta)


########
#
#   ENVELOP
#
##########


def envelop_span(envelope, span):
    return envelope.start <= span.start and span.stop <= envelope.stop


def envelop_spans(envelope, spans):
    for span in spans:
        if envelop_span(envelope, span):
            yield span


##########
#
#    ALIGN
#
############


def filter_misaligned_spans(envelopes, spans):
    starts = {_.start for _ in spans}
    stops = {_.stop for _ in spans}
    for span in envelopes:
        if span.start in starts and span.stop in stops:
            yield span


##########
#
#    OVERLAP
#
##########


def filter_overlapping_spans(spans):
    previous = None
    spans = sorted(spans, key=lambda _: (_.start, -_.stop))
    for span in spans:
        if previous and previous.stop > span.start:
            continue
        yield span
        previous = span


def split_overlapping_spans(spans):
    order = {}
    for index, span in enumerate(spans):
        order[id(span)] = index

    intervals = Intervals()
    for span in spans:
        intervals.addi(span.start, span.stop, span)

    intervals.split_overlaps()

    groups = defaultdict(list)
    for start, stop, span in intervals:
        groups[start, stop].append(span)

    for start, stop in sorted(groups):
        spans = groups[start, stop]
        spans = sorted(spans, key=lambda _: order[id(_)])
        type = spans[-1].type
        yield Span(start, stop, type)


########
#
#   TYPE
#
##########


def select_type_spans(spans, types):
    for span in spans:
        if span.type in types:
            yield span


def convert_span_types(spans, types):
    for span in spans:
        type = span.type
        if type not in types:
            raise KeyError('missing: %r, types: %r' % (type, sorted(types)))
        yield Span(
            span.start,
            span.stop,
            types[type]
        )


###########
#
#   STRIP
#
#########


def strip_span(span, text, chars):
    chunk = text[span.start:span.stop]
    word = chunk.strip(chars)
    size = len(word)
    offset = chunk.find(word)
    start = span.start + offset
    stop = start + size
    return Span(start, stop, span.type)


def strip_spans(spans, text, chars):
    for span in spans:
        yield strip_span(span, text, chars)


def strip_span_bounds(span, text, chars):
    span_ = strip_span(span, text, chars)
    # check both sides stripped
    if span_.start > span.start and span_.stop < span.stop:
        return span_  # "Lukoil"
    return span  # OOO "Lukoil"


def strip_spans_bounds(spans, text, chars):
    for span in spans:
        yield strip_span_bounds(span, text, chars)


def filter_empty_spans(spans):
    for span in spans:
        if span.start != span.stop:
            yield span


##########
#
#   SORT
#
#######


def sort_spans(spans):
    return sorted(spans, key=lambda _: _.start)
