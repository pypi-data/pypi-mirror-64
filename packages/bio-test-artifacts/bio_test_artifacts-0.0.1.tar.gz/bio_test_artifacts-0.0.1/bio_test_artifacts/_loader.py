import tempfile
import shutil
import os


class Load:

    _temp_path = None
    _temp_files = None

    @classmethod
    def copy_test_file(cls, file):
        cls._check_init()

        # Make sure the file is an absolute path
        file = os.path.abspath(os.path.expanduser(file))

        # Make a temp file and close the file descriptor
        _, extension = os.path.splitext(file)
        fd, tmp_file_name = tempfile.mkstemp(suffix=extension, dir=cls._temp_path.name)
        os.close(fd)

        # Copy the test file
        shutil.copy(file, tmp_file_name)

        cls._temp_files.append((file, tmp_file_name))

        return tmp_file_name

    @classmethod
    def make_test_file(cls, prefix=None, suffix=None):
        cls._check_init()

        # Make a temp file and close the file descriptor
        fd, tmp_file_name = tempfile.mkstemp(prefix=prefix, suffix=suffix, dir=cls._temp_path.name)
        os.close(fd)

        cls._temp_files.append((None, tmp_file_name))

        return tmp_file_name

    @classmethod
    def _check_init(cls):
        if cls._temp_path is None:
            cls._temp_path = tempfile.TemporaryDirectory(prefix="bio_test_")

        if cls._temp_files is None:
            cls._temp_files = []