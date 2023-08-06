#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
count_fgs_sam Unit Tests
========================

Performs the following tests:
    - Loading the script with no options
    - Loading the script with --version
    - Running the script with various options using a test input file. The
      output of the script is compared line-by-line to reference output files.

To run tests, use one of these commands:
|   python -m unittest discover
|   python -m count_fgs_sam.tests.test_count_fgs_sam

The reference output files can be (re)generated with the following command.
Suggest manually checking these output files (using git to easily see changes)
prior to packaging these in a new version:
|   python -m count_fgs_sam.tests.test_count_fgs_sam --generate

"""


import unittest
import io
import itertools
import sys
import warnings

from count_fgs_sam.count_fgs_sam import main as count_fgs_sam_main

tests_root = 'count_fgs_sam/tests/'
input_test_file = tests_root + 'NTCreads+rnd_align-Brunello_NTCs_mismatch___all.bam'

test_sets = [
    # tuples of (options, expected output file,  [generate])
    # generate is optional, if False, then the results will not be generated
    # for this test set

    # default
    ([input_test_file], 'output_default.tsv'),

    # output parameters
    ([input_test_file,'-d'], 'output_default_detailed.tsv'),
    ([input_test_file, '--show-unacceptable'], 'output_unacceptable.tsv'),
    ([input_test_file, '--show-ambiguous'], 'output_ambiguous.tsv'),
    ([input_test_file, '--show-length'], 'output_length.tsv'),

    # redundant score or length options (same as disabling these)
    ([input_test_file,'-c','200'], 'output_default.tsv', False),
    ([input_test_file,'-m','20'], 'output_default.tsv', False),
    ([input_test_file,'-M','20'], 'output_default.tsv', False),

    ([tests_root+"NTCreads+rnd_1000_align-Brunello_NTCs_mismatch___all.bam"], 'output1000_default.tsv'),
    # check QC fail/duplicates ignored, should return same as above
    ([tests_root+"NTCreads+rnd_1000_align-Brunello_NTCs_mismatch_3fail_5dup___all.bam"], 'output1000_default.tsv', False),
    # check paired are processed, should return same as above
    ([tests_root+"NTCreads+rnd_1000_align-Brunello_NTCs_mismatch_8paired___all.bam","-v"], 'output1000_default.tsv', False),

    # score parameters
    ([input_test_file,'-p','201'], 'output_p201.tsv'),

    ([input_test_file,'-c','194'], 'output_c194.tsv'),
    ([input_test_file,'-c','189'], 'output_c189.tsv'),

    ([input_test_file,'-a','10'], 'output_a10.tsv'),

    # length parameters
    ([input_test_file,'-l','19'], 'output_l19.tsv'),
    ([input_test_file,'-l','19','-p','189','--show-length'], 'output_l19p189_length.tsv'),
    ([input_test_file,'-m','19'], 'output_m19.tsv'),
    ([input_test_file,'-M','21'], 'output_M21.tsv'),
    ([input_test_file,'-m','19','-M','21','--show-length'], 'output_m19M21_length.tsv'),

    ([input_test_file,'-m','19','-c','189'], 'output_m19c185.tsv'),
    ([input_test_file,'-M','21','-c','189'], 'output_M21c185.tsv'),
    ([input_test_file,'-m','19','-M','21','-c','189'], 'output_m19M21c185.tsv'),

    # combined parameters
    ([input_test_file,
        '--perfectscore','200',
        '--expectedlength','20',
        '--unambiguous','3',
        '--acceptablescore','189',
        '--acceptableminlength','19',
        '--acceptablemaxlength','21',
        ], 'output_optimal.tsv'),

    ([input_test_file,
        '--perfectscore','200',
        '--expectedlength','20',
        '--unambiguous','3',
        '--acceptablescore','189',
        '--acceptableminlength','19',
        '--acceptablemaxlength','21',
        '--detailed'
        ], 'output_optimal_detailed.tsv'),
]

warning_test_sets = [
    # tuples of (options, warning, expected warning regex)
    # Note: -v is always appended to properly catch warnings
    #       needed due to overriding showwarning in main script

    ([tests_root + "NTCreads+rnd_1000_align-Brunello_NTCs_redundant___all.bam"],
        UserWarning,
        "ambiguous perfect"),
    ([tests_root + "NTCreads+rnd_1000_align-simple_decoys___all.bam"],
        UserWarning,
        "reference.*not.*expected length"),
    ([tests_root + "NTCreads+rnd_1000_align-Brunello_NTCs_mismatch___all_k5.bam"],
        UserWarning,
        "alignment.*ignored"),
    ([tests_root + "NTCreads+rnd_1000_align-Brunello_NTCs_fewRC___all.bam"],
        UserWarning,
        "reverse"),
    ([tests_root + "NTCreads+rnd_1000_align-Brunello_NTCs_mismatch_8paired___all.bam"],
        UserWarning,
        "paired")
]






class TestCountFGSSam(unittest.TestCase):
    def test_loading(self):
        # test loading main script
        with self.assertRaises(SystemExit) as cm:
            count_fgs_sam_main([])
        self.assertEqual(cm.exception.code, 2,'Unexpected return code')
    def test_loading_version(self):
        with self.assertRaises(SystemExit) as cm:
            count_fgs_sam_main(['--version'])
        self.assertEqual(cm.exception.code, 0,'Unexpected return code')
    def test_output(self):
        # generic tests for comparing output with set of options to an output file
        # output result cached as string object returned by main function

        for test_set in test_sets:
            test_options, test_expected_output_file = test_set[:2]
            flat_test_options = " ".join(test_options)
            test_expected_output_path = tests_root + test_expected_output_file
            with self.subTest(options = flat_test_options,
                              reference_file = test_expected_output_file):
                print("Testing options {}, comparing output to {}:".format(
                    flat_test_options,
                    test_expected_output_file))
                test_result = count_fgs_sam_main(test_options)
                test_stringio = io.StringIO(test_result)
                with open(test_expected_output_path,'r') as expected_obj:
                    for line_index,(test_line,expected_line) in enumerate(
                        itertools.zip_longest(test_stringio,expected_obj),1):
                        self.assertEqual(test_line.strip('\r\n'),
                            expected_line.strip('\r\n'),
                            '{} vs {}, line {} mismatch'.format(test_options,
                                test_expected_output_file, line_index))
    def test_warnings(self):
        # generic tests for testing warnings are produced

        for warning_test_set in warning_test_sets:
            test_options, warning, test_warning_regex = warning_test_set
            test_options.append("-v") # needed due to overriding showwarning in main script
            flat_test_options = " ".join(test_options)
            with self.subTest(options = flat_test_options,
                              warning = warning,
                              warning_regex = test_warning_regex):
                print("Testing options {} for warning {}:".format(flat_test_options,
                    test_warning_regex))
                with self.assertWarnsRegex(warning, test_warning_regex):
                    count_fgs_sam_main(test_options)


# this funciton will generate results files, instead of checking against them
# will be run if called with option --generate
def generate_results():
    for test_set in test_sets:
        if len(test_set)>2: # third parameter == False, don't generate
            if test_set[2]  == False:
                continue
        test_options, test_expected_output_file = test_set[:2]
        test_expected_output_path = tests_root + test_expected_output_file
        test_options.extend(['-o',test_expected_output_path])
        print("Running with options {}:".format(' '.join(test_options)))
        count_fgs_sam_main(test_options)

if __name__ == '__main__':
    if '--generate' in sys.argv:
        do_generate = True
    else:
        do_generate = False
    if do_generate: generate_results()
    else: unittest.main()
