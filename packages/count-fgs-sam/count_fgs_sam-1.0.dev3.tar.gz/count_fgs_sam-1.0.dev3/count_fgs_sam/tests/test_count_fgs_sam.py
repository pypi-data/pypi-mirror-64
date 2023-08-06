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

from count_fgs_sam.count_fgs_sam import main as count_fgs_sam_main

tests_root = 'count_fgs_sam/tests/'
input_test_file = tests_root + 'NTCreads+rnd_align-Brunello_NTCs___all.bam'
test_sets = [ # sets of (options, expected output file)

    # default
    ([input_test_file], 'output_default.tsv'),

    # output parameters
    ([input_test_file,'-d'], 'output_default_detailed.tsv'),
    ([input_test_file, '--show-unacceptable'], 'output_unacceptable.tsv'),
    ([input_test_file, '--show-ambiguous'], 'output_ambiguous.tsv'),
    ([input_test_file, '--show-length'], 'output_length.tsv'),

    # score parameters
    ([input_test_file,'-p','201'], 'output_p201.tsv'),

    ([input_test_file,'-c','194'], 'output_c194.tsv'),
    ([input_test_file,'-c','189'], 'output_c189.tsv'),

    ([input_test_file,'-a','10'], 'output_a10.tsv'),

    # length parameters
    ([input_test_file,'-l','19'], 'output_l19.tsv'),
    ([input_test_file,'-m','19'], 'output_m19.tsv'),
    ([input_test_file,'-M','21'], 'output_M21.tsv'),
    ([input_test_file,'-m','19','-M','21'], 'output_m19M21.tsv'),

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
    def test_processing_default(self):
        # generic tests for comparing output with set of options to an output file
        # output result cached as string object returned by main function

        for test_set in test_sets:
            test_options, test_expected_output_file = test_set
            test_expected_output_path = tests_root + test_expected_output_file
            print("Testing options {} vs {}:".format(test_options,
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

# this funciton will generate results files, instead of checking against them
# will be run if called with option --generate
def generate_results():
    for test_set in test_sets:
        test_options, test_expected_output_file = test_set
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
