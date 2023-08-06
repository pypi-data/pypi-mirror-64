import enum
from aioprometheus import Counter, Gauge, Summary, Histogram


class MetricsTypes(enum.Enum):
    counter = Counter
    gauge = Gauge
    summary = Summary
    untyped = None
    histogram = Histogram
