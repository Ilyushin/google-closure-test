#!/usr/bin/python2.7

import os, sys

main_dir = os.path.dirname(__file__)

# set path to tests
path_tests = os.path.join(main_dir, 'tests')
if not os.path.exists(path_tests):
    sys.exit("Folder of tests is missing")

# set path to a result folder
path_results = os.path.join(main_dir, 'results')
if not os.path.exists(path_tests):
    os.makedirs(path_results)


def get_size(path_to_file):
    return os.path.getsize(path_to_file)


class TestFile:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.size_before = get_size(path_to_file)
        self.size_after = 0


tests = []
for fn in os.listdir(path_tests):
    if fn.lower().endswith('.js'):
        tests.append(TestFile(path_tests + '/' + fn))


print tests