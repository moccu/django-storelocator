import csv


def unicode_csv_reader(file, dialect, **kwargs):
    csv_reader = csv.reader(file, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


class UnicodeCSVImporter(object):

    """
    Base csv importer class. Reads unicode rows into self.rows
    """

    def __init__(self, file, **kwargs):
        self.rows = [row for row in unicode_csv_reader(
            open(file, 'r'), **kwargs)]

    def run(self):
        raise NotImplementedError
