import csv
import sys

import fiona

from itertools import chain, islice
from typing import Dict, Iterable, Any

from geomet import wkt

csv.field_size_limit(sys.maxsize)


def grouper(n, iterable):
    """https://stackoverflow.com/a/8991553/4453925"""
    it = iter(iterable)
    while True:
       chunk = tuple(islice(it, n))
       if not chunk:
           return
       yield chunk


class wkt_dialect(csv.unix_dialect):
    delimiter = '|'
    quoting = csv.QUOTE_MINIMAL


def create_line(feature: Dict[str, Any]) -> Iterable:
    return chain([feature['id']], map(str, feature['properties'].values()), [wkt.dumps(feature['geometry'])])


def list_fields(src: fiona.Collection) -> list:
    return list(chain(['id'], map(lambda n: n.lower(), src.schema['properties'].keys()), ['wkt']))


def convert_to_wkt(input_file, output_file):
    with fiona.open(input_file) as src, \
            open(output_file, 'w') as output_fobj:
        writer = csv.writer(output_fobj, dialect=wkt_dialect)
        writer.writerow(list_fields(src))

        for group in grouper(1000, src):
            writer.writerows(map(create_line, group))
