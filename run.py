#!/usr/bin/python2.7

import os, sys, subprocess, time, csv

# set path to a main directory
main_dir = os.path.dirname(__file__)

# set path to the closure
path_closure = os.path.join(main_dir, 'compiler.jar')

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
        self.file_name = os.path.splitext(os.path.basename(path_to_file))[0]
        self.path_to_file = path_to_file
        self.perc_dec_size = 0  # calculation of percentage decrease size
        self.perc_dec_time = 0  # calculation of percentage decrease execution time


tests = []
for fn in os.listdir(path_tests):
    if fn.lower().find('opt') == -1 and fn.lower().endswith('.js'):
        tests.append(TestFile(path_tests + '/' + fn))
    else:
        os.remove(path_tests + '/' + fn)


for test_file in tests:

    size_before = get_size(test_file.path_to_file)
    opt_file = os.path.join(path_tests, test_file.file_name + '_opt.js')
    cmd_closure = 'java -jar ' + path_closure + ' --compilation_level ADVANCED_OPTIMIZATIONS' + ' --js ' + test_file.path_to_file + ' --js_output_file ' + opt_file
    r1 = subprocess.call(cmd_closure, shell=True)
    size_after = get_size(opt_file)

    if size_before > size_after:
        test_file.perc_dec_size = 100 - (size_after * 100 / size_before)

    # execute an unoptimized test
    start = time.time()
    cmd_node = 'node ' + test_file.path_to_file
    end = time.time()
    time1 = end - start

    # execute an optimized test
    start = time.time()
    cmd_node = 'node ' + opt_file
    end = time.time()
    time2 = end - start

    if time2 < time1:
        test_file.perc_dec_time = 100 - (time2 * 100 / time1)

csvfile = open(path_results + '/result.csv', 'w+')
csv_writer = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_NONE, escapechar=' ', quotechar='')
csv_writer.writerow(['test', ';dec size(%)', ';dec time(%)'])
all_time, all_size, amount = 0, 0, 0

for test_file in tests:
    newStr = []
    newStr.append(test_file.file_name)
    newStr.append(';' + str(test_file.perc_dec_size))
    newStr.append(';' + str(test_file.perc_dec_time))
    csv_writer.writerow(newStr)
    all_time += test_file.perc_dec_time
    all_size += test_file.perc_dec_size
    amount += 1
csv_writer.writerow(['', ';'+str(all_size/amount), ';'+str(all_time/amount)])
csvfile.close()
print "Finish"