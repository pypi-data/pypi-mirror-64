#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Count Functional Genomics Screen alignments in a SAM/BAM file with filtering
----------------------------------------------------------------------------

This program will count the alignments in a SAM/BAM file. The number of primary
alignments that are mapped to each reference sequence are counted. The
alignments are filtered for various criteria before counting, and (optionally)
additional buckets of counts (for each reference) are produced.

This script uses the [pysam] module. It is designed for alignments produced by
[Bowtie 2], and relies on the AS and XS score tags.

[pysam]: https://github.com/pysam-developers/pysam
[Bowtie 2]: http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml

"""

_PROGRAM_NAME = 'count_fgs_sam'
# -------------------------------------------------------------------------------
# Author:       Tet Woo Lee
#
# Created:      2020-03-12
# Copyright:    © 2020 Tet Woo Lee
# Licence:      GPLv3
#
# Dependencies: pysam, tested with v0.15.4
# -------------------------------------------------------------------------------

_PROGRAM_VERSION = '1.0.dev3'
# -------------------------------------------------------------------------------
# ### Change log
#
# + version 1.0.dev3 2020-03-26
#   First production version
#    - added unit tests
#    - PyPi and conda packaging
#    - add additional output options
#
#
# + version 1.0.dev2 2020-03-17
#   Modifications to improve performance, total 5.5x speedup:
#     - 468 s to 350 s (6.4M reads) by switching from Flag to IntFlag
#     - 350 s to 134 s by modifying to use int rather than IntFlag in add_counts
#     - 134 s to 85 s by modifying to use int with flag addition or operations
#     - Further improvements possible, e.g. 70 s possible by Cythonizing as-is
#       but current performance should suffice.
#
#
# + version 1.0.dev1 2020-03-15
#   First working version
# -------------------------------------------------------------------------------

# TODO in next version:
# Check: Secondary alignments ignored
# Check: Additional Alignment flags?
# Check: Warning for ambiguous alignments
# Check: Current test data file has no alternative scores. Generate some for testing.
# Add? Warning for reference of different length to expected


import sys
import argparse
import functools
import mimetypes
import csv
import io
from enum import Enum, IntFlag, auto

import pysam

class RawDescription_ArgumentDefaultsHelpFormatter(
    argparse.RawDescriptionHelpFormatter,
    argparse.ArgumentDefaultsHelpFormatter):
    pass
    """
    Combined HelpFormatter class for keeping raw description as well
    as formatting argument defaults using mutiple inheritance.
    Works with Python 3.7.6 as implementation methods of these classes do not
    interfere with each other, but since implementation of these classes
    are considered 'implementation details', there is no guarantee
    that this will keep working in the future.
    """

def main(argv = None, command_line = False):
        # command_line = True should be called if this script is being called from the
        # command line, and needs to output results to stdout if -o is absent
    if argv is None: argv = sys.argv[1:] # if parameters not provided, use sys.argv

    _ref_name_key = 'ref-name'
    _ref_length_key = 'ref-length'

    # INITIALISATION

    parser = argparse.ArgumentParser(prog=_PROGRAM_NAME,
                                     description=__doc__,
                                     formatter_class=RawDescription_ArgumentDefaultsHelpFormatter)
    parser_required_named = parser.add_argument_group('required named arguments')
    parser.add_argument('--version', action='version',
                        version='{} {}'.format(_PROGRAM_NAME, _PROGRAM_VERSION))
    parser.add_argument('inputfile',
                        help='Input SAM/BAM file, type determined by extension')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Do verbose logging')

    parser.add_argument('-p', '--perfectscore', type=int, default=200,
                        help='Cutoff for perfect alignments, must have alignment '
                        ' score (AS) of at least this (AS>=cutoff)')
    parser.add_argument('-l', '--expectedlength', type=int, default=20,
                        help='Expected length of reads, reads filtered by this length '
                        '(length==expectedlength)')
    parser.add_argument('-a', '--unambiguousdelta', type=int, default=3,
                        help='Cutoff for unambiguous alignments, reads filtered for '
                        'unambiguous alignments that have alignment score (AS) minus '
                        'alternative score (XS) less than equal this (AS-XS<=cutoff), '
                        'XS assumed to be 0 if not present for an alignment')
    parser.add_argument('-c', '--acceptablescore', type=int,
                        help='Cutoff for acceptable alignments AS>=cutoff; '
                        'if added, counts of acceptable reads are shown')
    parser.add_argument('-m', '--acceptableminlength', type=int,
                        help='Minimum length for acceptable alignments '
                        '(length >=minlength); if added, counts of shorter '
                        'reads are reported')
    parser.add_argument('-M', '--acceptablemaxlength', type=int,
                        help='Maximum length for acceptable alignments '
                        '(length <=maxlength); if added, counts of longer '
                        'reads are reported')

    # Show acceptable, shorter and longer are redundant options
    # They are automatically enabled with correct parameters
    # and have no use if those parameters absent
    # So these have been removed
    output_options = parser.add_argument_group(
                        title="optional output options",
                        description="Options to included additional count buckets in output")
    output_options.add_argument(
                        '-o', '--outputfile',
                        help='Output TSV file, output to stdout if absent')
    # output_options.add_argument(
    #                     '--show-acceptable', action='store_true',
    #                     help='Show counts of acceptable alignments')
    output_options.add_argument(
                        '--show-unacceptable', action='store_true',
                        help='Show counts of ambiguous alignments')
    output_options.add_argument(
                        '--show-ambiguous', action='store_true',
                        help='Show counts of unacceptable alignments')
    # output_options.add_argument(
    #                     '--show-shorter', action='store_true',
    #                     help='Show counts of shorter reads (>=minlength and '
    #                     '<expectedlength), implies --show-length')
    # output_options.add_argument(
    #                     '--show-longer', action='store_true',
    #                     help='Show counts of longer reads (<=maxlength and '
    #                     '>expectedlength), implies --show-length')
    output_options.add_argument(
                        '--show-length', action='store_true',
                        help="Show overall counts of reads by length classes, "
                        "not filtered by any other criteria; counts outside "
                        "specified lengths counted as 'other' length")
    output_options.add_argument('-d', '--detailed', action='store_true',
                        help='Turn on all optional counts (--show* options enabled, '
                        'as well as any counts enabled with additional threshold '
                        'parameters). Note that optional counts may all be '
                        'zero if matching parameters are not used.')

    args = parser.parse_args(argv)


    input_path = args.inputfile
    output_path = args.outputfile

    perfect_score = args.perfectscore
    expected_length = args.expectedlength
    acceptable_score = args.acceptablescore if args.acceptablescore else perfect_score
    acceptable_minlength = args.acceptableminlength if args.acceptableminlength is not None else expected_length
    acceptable_maxlength = args.acceptablemaxlength if args.acceptablemaxlength is not None else expected_length
        # defaults if not present prevent counting of these
    ambiguous_delta = args.unambiguousdelta

    show_unacceptable = args.show_unacceptable or args.detailed
    show_ambiguous = args.show_ambiguous or args.detailed
    show_shorter = args.detailed or (args.acceptableminlength is not None)
    show_longer = args.detailed or (args.acceptablemaxlength is not None)
    show_length = args.show_length or args.detailed
    show_acceptable = args.detailed or (args.acceptablescore is not None)

    verbose = args.verbose

    assert acceptable_minlength<=expected_length, "min length is not <= expected"
    assert acceptable_maxlength>=expected_length, "max length is not >= expected"

    print('{} {}'.format(_PROGRAM_NAME, _PROGRAM_VERSION))
    print("Input file: {}".format(input_path))
    print("Output file: {}".format(output_path))
    print("Perfect score (>=): {}".format(perfect_score))
    print("Perfect length (==): {}".format(expected_length))
    if show_acceptable: print("Acceptable score (>=): {}".format(acceptable_score))
    if show_shorter: print("Acceptable shorter length: >={} and <{}".format(acceptable_minlength,expected_length))
    if show_longer: print("Acceptable longer length: >{} and <={}".format(expected_length,acceptable_maxlength))
    if show_length: print("Other length: <{} or >{}".format(acceptable_minlength,acceptable_maxlength))
    print("Unambiguous delta (>): {}".format(ambiguous_delta))
    if show_ambiguous: print("Ambiguous delta (<=): {}".format(ambiguous_delta))
    if show_acceptable: print("Showing acceptable counts")
    if show_unacceptable: print("Showing unacceptable counts")
    if show_ambiguous: print("Showing ambiguous counts")
    if show_shorter: print("Showing shorter counts")
    if show_longer: print("Showing longer counts")
    if show_length: print("Showing overall counts by length")
    if verbose: print("Showing verbose logging")

    mimetypes.add_type('application/bam','.bam')
    mimetypes.add_type('text/sam','.sam')

    # HELPER FUNCTIONS

    # openers for input and output files
    if mimetypes.guess_type(input_path)[0] == 'application/bam':
        input_openmode = 'rb'
    else:
        input_openmode = 'r'

    # Store flags of a read
    # with certain combinations of flags defining buckets for output
    class Buckets(IntFlag):
        ANY = 0 # no flags set
        # Flags
        # Alignment score: perfect, acceptable, unacceptable
        SCORE_PERFECT = auto()
        SCORE_ACCEPTABLE = auto()
        SCORE_UNACCEPTABLE = auto()
        # Read length: good, shorter, longer, other (expected to be empty)
        LENGTH_GOOD = auto()
        LENGTH_SHORTER = auto()
        LENGTH_LONGER = auto()
        LENGTH_OTHER = auto()
        # Alignment delta: unambiguous, ambiguous
        DELTA_UNAMBIGUOUS = auto()
        DELTA_AMBIGUOUS = auto()
        DELTA_UNDEFINED = auto() # set when it cannot be defined, e.g. unmapped reads

        # Buckets of combined flags
        PERFECT_UNAMBIGUOUS_LENGTH     = SCORE_PERFECT      | LENGTH_GOOD    | DELTA_UNAMBIGUOUS
            # 'length' as shorthand for 'good length'
        ACCEPTABLE_UNAMBIGUOUS_LENGTH  = SCORE_ACCEPTABLE   | LENGTH_GOOD    | DELTA_UNAMBIGUOUS
        ACCEPTABLE_UNAMBIGUOUS_SHORTER = SCORE_ACCEPTABLE   | LENGTH_SHORTER | DELTA_UNAMBIGUOUS
        ACCEPTABLE_UNAMBIGUOUS_LONGER  = SCORE_ACCEPTABLE   | LENGTH_LONGER  | DELTA_UNAMBIGUOUS

        PERFECT_AMBIGUOUS_LENGTH       = SCORE_PERFECT      | LENGTH_GOOD    | DELTA_AMBIGUOUS
        ACCEPTABLE_AMBIGUOUS_LENGTH    = SCORE_ACCEPTABLE   | LENGTH_GOOD    | DELTA_AMBIGUOUS
        ACCEPTABLE_AMBIGUOUS_SHORTER   = SCORE_ACCEPTABLE   | LENGTH_SHORTER | DELTA_AMBIGUOUS
        ACCEPTABLE_AMBIGUOUS_LONGER    = SCORE_ACCEPTABLE   | LENGTH_LONGER  | DELTA_AMBIGUOUS

        UNACCEPTABLE_LENGTH            = SCORE_UNACCEPTABLE | LENGTH_GOOD
        UNACCEPTABLE_SHORTER           = SCORE_UNACCEPTABLE | LENGTH_SHORTER
        UNACCEPTABLE_LONGER            = SCORE_UNACCEPTABLE | LENGTH_LONGER
        UNACCEPTABLE_OTHER             = SCORE_UNACCEPTABLE | LENGTH_OTHER

        # get 'good' name for a bucket
        # coded only for buckets of interest
        def get_goodname(self):

            if self==self.LENGTH_GOOD:
                return 'expected-length'
            elif self==self.LENGTH_SHORTER:
                return 'shorter'
            elif self==self.LENGTH_LONGER:
                return 'longer'
            elif self==self.LENGTH_OTHER:
                return 'length-out-of-range'

            bucket_str = str(self)
            bucket_name = bucket_str.split('.')[1] # retrieve part after class name
            if '|' in bucket_name: return bucket_name # don't convert names of unnamed combinations
            bucket_name = bucket_name.lower().replace('_','/').replace(
                'length','expected-length').replace('other','length-out-of-range')

            return(bucket_name)

        # adds a count for each bucket_to_count to datadict if flags match
        # also track:
        # everything = always counted
        # total = whatever was added to a datadict
        # exclude = whatever wasn't added to datadict
        # also adds counts to everythingdict and excludedict
        def add_counts(self, buckets_to_count, datadict, everythingdict,
            totaldict, excludedict):
            self_int = int(self)
            for bucket_to_count in buckets_to_count:
                if (self_int & bucket_to_count) == bucket_to_count:
                    # note, need == comparison as otherwise empty flag bucket won't count

                    # if matches flags, add count
                    # also add to total
                    datadict[bucket_to_count] += 1
                    totaldict[bucket_to_count] += 1
                else:
                    # doesn't match, add to exclude count
                    excludedict[bucket_to_count] += 1
                everythingdict[bucket_to_count] += 1 # always count

    # initialise datadict to have int members with value 0 for each bucket_to_init
    def init_counts(buckets_to_init, datadict):
        for bucket_to_init in buckets_to_init:
            assert bucket_to_init not in datadict, "reinitalising dict"
            datadict[bucket_to_init] = 0

    # buckets_of_interest for output
    # these are as original Enum (or IntFlag) objects
    # select buckets based on options provided
    buckets_of_interest_enum = [Buckets.PERFECT_UNAMBIGUOUS_LENGTH]
    if show_acceptable:
        buckets_of_interest_enum.append(Buckets.ACCEPTABLE_UNAMBIGUOUS_LENGTH)
    if show_shorter: # acceptable shorter/longer occur with no acceptable score
        buckets_of_interest_enum.append(Buckets.ACCEPTABLE_UNAMBIGUOUS_SHORTER)
    if show_longer:
        buckets_of_interest_enum.append(Buckets.ACCEPTABLE_UNAMBIGUOUS_LONGER)
    if show_ambiguous:
        buckets_of_interest_enum.extend((Buckets.PERFECT_AMBIGUOUS_LENGTH,
                                         Buckets.ACCEPTABLE_AMBIGUOUS_LENGTH))
        if show_shorter:
            buckets_of_interest_enum.append(Buckets.ACCEPTABLE_AMBIGUOUS_SHORTER)
        if show_longer:
            buckets_of_interest_enum.append(Buckets.ACCEPTABLE_AMBIGUOUS_LONGER)
    if show_unacceptable:
        buckets_of_interest_enum.append(Buckets.UNACCEPTABLE_LENGTH)
        if show_shorter:
            buckets_of_interest_enum.append(Buckets.UNACCEPTABLE_SHORTER)
        if show_longer:
            buckets_of_interest_enum.append(Buckets.UNACCEPTABLE_LONGER)
        buckets_of_interest_enum.append(Buckets.UNACCEPTABLE_OTHER)
    if show_length:
        buckets_of_interest_enum.append(Buckets.LENGTH_GOOD)
        if show_shorter:
            buckets_of_interest_enum.append(Buckets.LENGTH_SHORTER)
        if show_longer:
            buckets_of_interest_enum.append(Buckets.LENGTH_LONGER)
        buckets_of_interest_enum.append(Buckets.LENGTH_OTHER)
    buckets_of_interest_enum.append(Buckets.ANY)

    # multiple & operations performed using buckets_of_interest
    # much more efficient if these are converted to Int
    # also store a lookup of int:(bucket, goodname) for easy conversion later
    buckets_of_interest_lookup = {}
    buckets_of_interest = []
    for bucket_of_interest in buckets_of_interest_enum:
        bucket_of_interest_int = int(bucket_of_interest)
        buckets_of_interest.append(bucket_of_interest_int)
        buckets_of_interest_lookup[bucket_of_interest_int] = (
            bucket_of_interest, bucket_of_interest.get_goodname()
        )

    # convert all enum values in Buckets to int in a new object
    # allows int these to be directly with | and & operations
    class IntBuckets(object):
        def __init__(self, other):
            for item in other:
                setattr(self,item.name, item.value)
    intBuckets = IntBuckets(Buckets)


    with open(input_path,input_openmode) as alignment_fileobj:
        samfile = pysam.AlignmentFile(alignment_fileobj)

        # Build list of reference sequences, storing each item as a dict
        # to hold arbitrary set of different data
        num_references = samfile.nreferences
        print("Number of alignment references: {}".format(num_references))
        reference_list = [{_ref_name_key: samfile.get_reference_name(tid)
                           } for tid in range(num_references)]
        for index,item in enumerate(reference_list):

            item[_ref_length_key] = samfile.get_reference_length(item[_ref_name_key])
                # pysam expects get_reference_length to supply a name, not tid
            assert samfile.get_reference_name(index) == item[_ref_name_key], "tid/name mismatch"
                # check reference_list[tid] returns correct item

        if verbose: # show all
            for tid,item in enumerate(reference_list):
                print("Reference {}: {} length {}".format(tid,item[_ref_name_key],item[_ref_length_key]))

        # for storing unmapped and various totals
        unmapped_dict = {_ref_name_key:'*unmapped',_ref_length_key:float('nan')}
            # unmapped reads, note these are often not counted, rather than
            # counted as unmapped
        total_dict = {_ref_name_key:'**total_counted',_ref_length_key:float('nan')}
            # total reads counted per reference or as unmapped
        exclude_dict = {_ref_name_key:'**excluded',_ref_length_key:float('nan')}
            # anything not counted, includes unmapped if unmapped if excluded
        everything_dict = {_ref_name_key:'***grand_total',_ref_length_key:float('nan')}
            # grand total reads
        reference_list.append(unmapped_dict)
        reference_list.append(total_dict)
        reference_list.append(exclude_dict)
        reference_list.append(everything_dict)

        # prepare for counting
        for item in reference_list: init_counts(buckets_of_interest,item)

        # function to determine read designation (index+name) when required
        # expects to find alignment_read and read_index in scope
        def get_read_designation():
            read_name = alignment_read.query_name
            if read_name is not None:
                read_designation = "{}: {}".format(read_index, read_name)
            else:
                read_designation = "Unnamed {}".format(read_index)
            return read_designation

        num_all = 0 # total entries in file
        num_reads = 0 # primary alignments/unmapped
        num_ignored = 0 # secondary/supplementary
        num_alternative_score = 0 # track number of alignments with alternative scores
        num_mapped = 0 # track number of reads that were mapped
        num_perfect_ambiguous = 0 # number of perfect ambiguous alignments

        # fetch each sequence, need to use until_eof to get unmapped
        for read_index,alignment_read in enumerate(samfile.fetch(until_eof = True), start=1):
            num_all+=1
            if alignment_read.is_secondary:
                if verbose: print("Warning, secondary alignment found for read {}, ignoring".format(get_read_designation()))
                num_ignored+=1
                continue
            if alignment_read.is_supplementary:
                if verbose: print("Warning, supplementary alignment found for read {}, ignoring".format(get_read_designation()))
                num_ignored+=1
                continue

            num_reads+=1 # primary only

            entry_bucket = int(intBuckets.ANY) # empty flags, use int for efficiency
            matched_reference = None

            read_length = alignment_read.infer_read_length()
            if read_length is None:
                if not alignment_read.is_unmapped:
                    raise IOError("Unable to infer read length for mapped read {}".format(get_read_designation()))
                else:
                    # for unmapped reads only, fall back to query length
                    if verbose: print("F")
                    read_length = alignment_read.query_length


            if read_length == expected_length:
                entry_bucket |= intBuckets.LENGTH_GOOD
            elif read_length <= expected_length and read_length >= acceptable_minlength:
                entry_bucket |= intBuckets.LENGTH_SHORTER
            elif read_length >= expected_length and read_length <= acceptable_maxlength:
                entry_bucket |= intBuckets.LENGTH_LONGER
            else:
                entry_bucket |= intBuckets.LENGTH_OTHER
                # may be empty if all >=min length and <=max length


            if alignment_read.is_unmapped:
                # unmapped reads are always unacceptable score
                entry_bucket |= intBuckets.SCORE_UNACCEPTABLE
                entry_bucket |= intBuckets.DELTA_UNDEFINED
                matched_reference = unmapped_dict

                alignment_score = None
                alternative_score = None
                delta = None

            else:
                num_mapped+=1
                matched_reference = reference_list[alignment_read.reference_id]

                if not alignment_read.has_tag('AS'):
                    raise IOError("Alignment does not contain tag AS, read {}".format(get_read_designation()))
                alignment_score = alignment_read.get_tag('AS')

                if alignment_read.has_tag('XS'):
                    alternative_score = alignment_read.get_tag('XS')
                    delta = alignment_score - alternative_score
                    num_alternative_score+=1
                else:
                    alternative_score = None
                    delta = alignment_score # assume alternative is 0 if absent

                assert delta>=0, "delta is <0"

                if alignment_score >= perfect_score:
                    if entry_bucket & intBuckets.LENGTH_GOOD:
                        # only good length entries can be 'perfect'
                        entry_bucket |= intBuckets.SCORE_PERFECT
                    elif entry_bucket & intBuckets.LENGTH_SHORTER or entry_bucket & intBuckets.LENGTH_LONGER:
                        entry_bucket |= intBuckets.SCORE_ACCEPTABLE
                    else:
                        entry_bucket |= intBuckets.SCORE_UNACCEPTABLE
                elif alignment_score >= acceptable_score:
                    entry_bucket |= intBuckets.SCORE_ACCEPTABLE
                else:
                    entry_bucket |= intBuckets.SCORE_UNACCEPTABLE

                if delta > ambiguous_delta:
                    entry_bucket |= intBuckets.DELTA_UNAMBIGUOUS
                else:
                    entry_bucket |= intBuckets.DELTA_AMBIGUOUS

                if entry_bucket == intBuckets.PERFECT_AMBIGUOUS_LENGTH:
                    num_perfect_ambiguous+=1

            entry_bucket = Buckets.ANY | entry_bucket # convert back to Buckets

            entry_bucket.add_counts(buckets_of_interest,
                datadict = matched_reference,
                everythingdict = everything_dict,
                totaldict = total_dict,
                excludedict = exclude_dict
                )

            if verbose:
                print("Read: {}; Aligned to: {}; Bucket: {};\n"
                      "Length: {}; Score AS: {}; Alternative XS: {}; Delta: {};".format(
                      get_read_designation(), matched_reference[_ref_name_key],
                      str(entry_bucket),
                      read_length, alignment_score, alternative_score, delta))
                print("Raw data:")
                print(alignment_read)

        # do some checks
        assert num_reads == everything_dict[Buckets.ANY], "mismatch total"
        assert num_mapped == num_reads - unmapped_dict[Buckets.ANY], "mismatch mapped count"
        assert num_mapped == num_reads - unmapped_dict[Buckets.ANY], "mismatch mapped count"
        assert all(
            everything_dict[bucket] == total_dict[bucket] + exclude_dict[bucket]
            for bucket in buckets_of_interest), "total/exclude/all count"
        if Buckets.PERFECT_AMBIGUOUS_LENGTH in total_dict:
            assert num_perfect_ambiguous==total_dict[Buckets.PERFECT_AMBIGUOUS_LENGTH], "mismatch perfect ambiguous count"

        # print summaries
        print("Summary of aligned reads:")
        print(" Entries: {}\n Processed + ignored (secondary/supplementary): {} + {}".format(
            num_all, num_reads, num_ignored
        ))
        print(" Mapped entries: {}\n With alternative scores: {}".format(
            num_mapped, num_alternative_score
        ))

        print("Summary of aligned counts:")
        print(" Total perfect alignments: {}".format(total_dict[Buckets.PERFECT_UNAMBIGUOUS_LENGTH]))
        print(" Total ambiguous perfect alignments: {}".format(num_perfect_ambiguous))
        if num_perfect_ambiguous>0:
            print (" Warning! >0 ambiguous perfect alignments, there may be duplicate entries among references")


        # get keys of datadict converted to good names if they are Buckets
        # uses the lookup generated previously
        def convert_dict_keys(datadict):
            ret = {}
            for key,value in datadict.items():
                newkey = buckets_of_interest_lookup[key][1] if isinstance(key, int) else key
                ret[newkey] = value
            return ret

        with io.StringIO() as out_buffer:
        #with open(output_path, 'w', newline='') as out_buffer:
            fieldnames = convert_dict_keys(everything_dict).keys()

            writer = csv.DictWriter(out_buffer, fieldnames=fieldnames, dialect = 'excel-tab')

            writer.writeheader()
            for item in reference_list:
                writer.writerow(convert_dict_keys(item))
            output = out_buffer.getvalue()

        if output_path is None:
            if command_line: print(output)
        else:
            with open(output_path, 'w') as out_tsvfile:
                out_tsvfile.write(output)

        return output

if __name__ == '__main__':
    main(command_line = True)
