#!/usr/bin/python2.7

import os, sys, subprocess, time, csv, timeit

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
        self.perc_dec_time_node = 0  # calculation of percentage decrease execution time for node.js
        self.perc_dec_time_v8 = 0  # calculation of percentage decrease execution time for v8
        self.size_before = 0
        self.size_after = 0
        self.exec_time_before_node = 0
        self.exec_time_after_node = 0
        self.exec_time_before_v8 = 0
        self.exec_time_after_v8 = 0


tests = []
for fn in os.listdir(path_tests):
    if fn.lower().find('opt') == -1 and fn.lower().endswith('.js'):
        tests.append(TestFile(path_tests + '/' + fn))
    else:
        os.remove(path_tests + '/' + fn)


for test_file in tests:

    print '********************************START**************************************'
    print str(test_file.path_to_file)
    
    #SIZE
    test_file.size_before = get_size(test_file.path_to_file)
    opt_file = os.path.join(path_tests, test_file.file_name + '_opt.js')
    cmd_closure = 'java -jar ' + path_closure + ' --compilation_level ADVANCED_OPTIMIZATIONS --summary_detail_level 0' + ' --js ' + test_file.path_to_file + ' --js_output_file ' + opt_file
    r1 = subprocess.call(cmd_closure, shell=True)
    test_file.size_after = get_size(opt_file)

    if test_file.size_before > test_file.size_after:
        test_file.perc_dec_size = 100-test_file.size_after * 100 / test_file.size_before
    else:
        test_file.perc_dec_size = -(100-test_file.size_before * 100 / test_file.size_after)

    #EXECUTION TIME
    
    #node.js
    # execute an unoptimized test
    start = time.time()    
    cmd_v8 = 'node '+ test_file.path_to_file
    subprocess.call(cmd_v8, shell=True, stderr=subprocess.STDOUT)
    end = time.time()
    
    test_file.exec_time_before_node = round((end - start) * 1000, 0)

    # execute an optimized test
    start = time.time()
    cmd_v8 = 'node '+ opt_file
    subprocess.call(cmd_v8, shell=True, stderr=subprocess.STDOUT)
    end = time.time()
    
    test_file.exec_time_after_node = round((end - start) * 1000, 0)
    
    if test_file.exec_time_after_node < test_file.exec_time_before_node:
        test_file.perc_dec_time_node = 100 - test_file.exec_time_after_node * 100 / test_file.exec_time_before_node
    else:
        test_file.perc_dec_time_node = -(100-test_file.exec_time_before_node * 100 / test_file.exec_time_after_node)
        
        
    #v8
    # execute an unoptimized test
    start = time.time()    
    cmd_v8 = '/Users/Evgeniy/Development/git/v8/out/x64.release/shell '+ test_file.path_to_file
    subprocess.call(cmd_v8, shell=True, stderr=subprocess.STDOUT)
    end = time.time()
    
    test_file.exec_time_before_v8 = round((end - start) * 1000, 0)

    # execute an optimized test
    start = time.time()
    cmd_v8 = '/Users/Evgeniy/Development/git/v8/out/x64.release/shell '+ opt_file
    subprocess.call(cmd_v8, shell=True, stderr=subprocess.STDOUT)
    end = time.time()
    
    test_file.exec_time_after_v8 = round((end - start) * 1000, 0)
    
    if test_file.exec_time_after_v8 < test_file.exec_time_before_v8:
        test_file.perc_dec_time_v8 = 100 - test_file.exec_time_after_v8 * 100 / test_file.exec_time_before_v8
    else:
        test_file.perc_dec_time_v8 = -(100-test_file.exec_time_before_v8 * 100 / test_file.exec_time_after_v8)
       
    print '********************************FINISH**************************************\n\n'
    
    
csvfile = open(path_results + "/result.csv", 'w+')
csv_writer = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_NONE, escapechar=' ', quotechar='')
csv_writer.writerow(['test', ';dec size(%)', ';dec time node.js(%)', ';dec time v8(%)', ';size before', ';size after', ';exec time before node', ';exec time after node', ';exec time before v8', ';exec time after v8'])
all_time_node, all_time_v8, all_size, amount = 0, 0, 0, 0

for test_file in tests:
    newStr = []
    newStr.append(test_file.file_name+".js")
    newStr.append(';' + str(test_file.perc_dec_size))
    newStr.append(';' + str(round(test_file.perc_dec_time_node,0))[:-2])
    newStr.append(';' + str(round(test_file.perc_dec_time_v8,0))[:-2])
    newStr.append(';' + str(test_file.size_before))
    newStr.append(';' + str(test_file.size_after))
    newStr.append(';' + str(test_file.exec_time_before_node))
    newStr.append(';' + str(test_file.exec_time_after_node))
    newStr.append(';' + str(test_file.exec_time_before_v8))
    newStr.append(';' + str(test_file.exec_time_after_v8))
    csv_writer.writerow(newStr)
    
    all_time_node += test_file.perc_dec_time_node
    all_time_v8 += test_file.perc_dec_time_v8
    all_size += test_file.perc_dec_size
    amount += 1
    
    
csv_writer.writerow(['', ';'+str(all_size/amount), ';'+str(round(all_time_node/amount))[:-2], ';'+str(round(all_time_v8/amount))[:-2]])
csvfile.close()
print "Finish"