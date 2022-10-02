from multiprocessing import cpu_count, Pool
import glob
from os import listdir, stat
from os.path import dirname, join
from datetime import datetime
from typing import List, Tuple
import re

"""
# CHANGELOG #

# 2022-10-02

# Added

- Implemented ignore functionality, with regex patterns.
- Implemented multithreading functionalities

# 2022-06-25

# Added

- Implemented the recursive functionality.

# 2022-06-24

# Added

- Created and developed the basic prototype to store the state of a messy folder.
- Store datetime in the folder.
- It can now store, in addition to the name, the size and the creation and update dates.
"""

BASEPATH = dirname(__file__)

IGNORE_REGEX = [
    re.compile(r'/node_modules/i'),
]

MULTITHREAD_WORKERS = cpu_count() - 1
FILES_COLLECTOR: List[str] = list()


def format_datetime(
    date: datetime = None,
    format: str = '%d-%m-%y %H-%M-%S',
    timestamp: int = None
) -> str:
    """
    Standarizes the date's format

    date : datetime
        The date to format
    format : str
        The format to be applied

    returns str
    """
    assert date is not None or timestamp is not None

    if not date and timestamp:
        date = datetime.fromtimestamp(int(timestamp))

    return date.strftime(format)


def get_filename(
    name: str = 'files',
    extension: str = 'txt',
) -> str:
    """
    Generates a filename

    name : str
        The default name of the file
    extension : str
        The default extension it'll be stored in

    returns str
    """
    current_time = datetime.now()
    current_time_str = format_datetime(current_time)

    return f'{name} - {current_time_str}.{extension}'


def prepare_files(
    data: Tuple[List[str], str]
) -> str:
    """
    Prepares the files with their sizes and last modification date

    data: Tuple[list, str]
        collector : List[str]
            The array with filenames to append the result to
        filename : str
            The name of the file to evaluate

    returns str
    """
    global FILES_COLLECTOR
    _, filename = data
    try:
        absolute_path = join(BASEPATH, filename)
        filedetails = stat(absolute_path)
        filesize = filedetails.st_size / 1024 / 1024
        creation_date = format_datetime(
            timestamp=filedetails.st_ctime,
            format='%d/%m/%y %H:%M:%S'
        )
        update_date = format_datetime(
            timestamp=filedetails.st_atime,
            format='%d/%m/%y %H:%M:%S'
        )

        real_filename = absolute_path.replace(join(BASEPATH, ''), '')
        processed_filename = f'{real_filename} - {round(filesize, 2)} MB - CREATION: {creation_date} - MODIFICATION: {update_date}'
        # FILES_COLLECTOR.append(processed_filename)

        filename = get_filename()
        full_filename_path = join(BASEPATH, filename)
        with open(full_filename_path, 'a+') as file_writer:
            file_writer.write(processed_filename)
            file_writer.write('\n')
    except:
        return f'Could not compute "{filename}"'


def filter_files(filename: str) -> bool:
    """
    Filters out all of the files that should be ignored

    filename: str
        The filename to evaluate

    returns bool
    """
    for path_to_ignore in IGNORE_REGEX:
        if path_to_ignore.search(filename):
            return False

    return True


def get_files_list(
    target_path: str = BASEPATH,
    recursive: bool = False
) -> List[str]:
    """
    Returns the list of files

    target_path : str
        The path it will operate in
    recursive : bool
        If it will collect them in a recursive manner or not

    returns List[str]
    """
    files = []

    if not recursive:
        files = listdir(target_path)
    else:
        files = []
        files = glob.glob(join(BASEPATH, '**/*.*'), recursive=True)

    return files


def main(
    bulk_write: bool = False
) -> None:
    """
    Stores the actual state of the files at the root level of this file's folder

    bulk_write : bool
        Not recomended for large chunks of files,
        it may be risky and there may be information loss due to crashes.
        False by default

    returns None
    """
    global FILES_COLLECTOR

    filename = get_filename()
    full_filename_path = join(BASEPATH, filename)
    print(f'Will be stored at: "{full_filename_path}"')

    with open(full_filename_path, 'w+') as file_writer:
        file_writer.write('')

    scanned_files: Tuple[List[str], str] = [
        (None, file)
        for file in get_files_list(BASEPATH, recursive=True)
        if filter_files(file)
    ]
    print('Files to evaluate', len(list(scanned_files)))

    with Pool(MULTITHREAD_WORKERS) as executor:
        executor.map(prepare_files, scanned_files)

    global FILES_COLLECTOR
    print(len(FILES_COLLECTOR))
    if not FILES_COLLECTOR:
        print('No files could be retrieved')
        return

    # preapred_files = map(prepare_files, scanned_files)
    with open(full_filename_path, 'w+') as file_writer:
        if not bulk_write:
            file_writer.write('\n'.join(FILES_COLLECTOR))
        else:
            for line in FILES_COLLECTOR:
                file_writer.write(line)
                file_writer.write('\n')


if __name__ == '__main__':
    main()
