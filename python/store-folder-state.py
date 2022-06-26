import glob
from os import listdir, stat
from os.path import dirname, join
from datetime import datetime
from typing import List

"""
# CHANGELOG #

## 2022-06-25

### Added

- Implemented the recursive functionality.

## 2022-06-24

### Added

- Created and developed the basic prototype to store the state of a messy folder.
- Store datetime in the folder.
- It can now store, in addition to the name, the size and the creation and update dates.
"""

BASEPATH = dirname(__file__)


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
    filename: str
) -> str:
    """
    Prepares the files with their sizes and last modification date

    filename : str
        The name of the file to evaluate

    returns str
    """
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
    return f'{real_filename} - {round(filesize, 2)} MB - CREATION: {creation_date} - MODIFICATION: {update_date}'


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


def main() -> None:
    """
    Stores the actual state of the files at the root level of this file's folder

    returns None
    """

    filename = get_filename()
    full_filename_path = join(BASEPATH, filename)
    print(f'Stored at: "{full_filename_path}"')

    files = map(prepare_files, get_files_list(BASEPATH, recursive=True))
    with open(full_filename_path, 'w+') as file_writer:
        file_writer.write('\n'.join(files))


if __name__ == '__main__':
    main()
