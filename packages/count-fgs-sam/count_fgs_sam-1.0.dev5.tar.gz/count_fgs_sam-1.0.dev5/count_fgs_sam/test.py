from count_fgs_sam.count_fgs_sam import main as count_fgs_sam_main

def main():
    count_fgs_sam_main(["count_fgs_sam/tests/NTCreads+rnd_1000_align-Brunello_NTCs_mismatch_3fail_5dup___all.bam"],return_result=True)

if __name__ == '__main__':
    main()
