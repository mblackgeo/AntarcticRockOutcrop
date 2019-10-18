import os
import csv

"""
This function loads the contents of the scene id list from Burton-Johnson et. al. into memory

@:param string file_path: the path to the text file

@:returns list of OrderedDicts: a list of dicts containing the contents of the text file.
                        Each item of the list is a dict with file headers as keys and row
                        values as values.
"""


def load_scene_ids(file_path):
    assert os.path.exists(file_path)

    with open(file_path, 'r') as tab_delim:
        reader = csv.DictReader(tab_delim, delimiter='\t')
        return [row for row in reader if row[list(row.keys())[0]]]
