import pandas as pd
import os
import subprocess
from bio_test_artifacts._loader import Load

_data_path = os.path.join(os.path.dirname(__file__), "artifacts")

_YEAST_COUNTS_TPM_FILE_NAME = "GSE135430_counts_TPM.tsv"
_YEAST_COUNTS_TPM_CHR01_FILE_NAME = "GSE135430_counts_chr01_TPM.tsv"
_YEAST_COUNTS_SINGLE_CELL_FILE_NAME = "GSE125162_counts_chr01.tsv"


def counts_yeast_tpm(gzip=False):
    """
    Make a count TSV file from GEO record GSE135430.
    This will have 12 non-header rows and 6685 gene columns. All values are floats.
    It is in Transcripts Per Million (TPM) and all rows should approximately sum to 1e6

    :param gzip: Provide a gzipped (.gz) file instead of a .tsv file. Defaults to False.
    :type gzip: bool
    :returns: An absolute path to the count TSV file and a pandas DataFrame (12 x 6685)
    :rtype: str, pd.DataFrame
    """
    file = os.path.join(_data_path, _YEAST_COUNTS_TPM_FILE_NAME)

    copied_file = Load.copy_test_file(file)

    if gzip:
        subprocess.check_call(['gzip', copied_file])
        copied_file += ".gz"

    return copied_file, pd.read_csv(file, sep="\t", index_col=None)


def counts_yeast_tpm_chr01(gzip=False):
    """
    Make a count TSV file from GEO record GSE135430.
    This will have 12 non-header rows and 121 gene columns. All values are floats.
    It is in Transcripts Per Million (TPM), but it is a subset of the entire genome and rows do not sum to 1e6.

    :param gzip: Provide a gzipped (.gz) file instead of a .tsv file. Defaults to False.
    :type gzip: bool
    :returns: An absolute path to the count TSV file and a pandas DataFrame (12 x 121)
    :rtype: str, pd.DataFrame
    """
    file = os.path.join(_data_path, _YEAST_COUNTS_TPM_CHR01_FILE_NAME)

    copied_file = Load.copy_test_file(file)

    if gzip:
        subprocess.check_call(['gzip', copied_file])
        copied_file += ".gz"

    return copied_file, pd.read_csv(file, sep="\t", index_col=None)


def counts_yeast_single_cell_chr01(gzip=False):
    """
    Make a count TSV file from GEO record GSE125162.
    This will have 38225 non-header rows and 121 gene columns. All values are integers.
    It is in (UMI) counts.

    :param gzip: Provide a gzipped (.gz) file instead of a .tsv file. Defaults to False.
    :type gzip: bool
    :returns: An absolute path to the count TSV file and a pandas DataFrame (38225 x 121)
    :rtype: str, pd.DataFrame
    """
    file = os.path.join(_data_path, _YEAST_COUNTS_SINGLE_CELL_FILE_NAME)

    copied_file = Load.copy_test_file(file)

    if gzip:
        subprocess.check_call(['gzip', copied_file])
        copied_file += ".gz"

    return copied_file, pd.read_csv(file, sep="\t", index_col=None)
