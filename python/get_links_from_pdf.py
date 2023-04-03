"""
Get the words from a PDF

python3 get_links_from_pdf.py /source/to/pdf

----------------------------

Example:
python3 get_links_from_pdf.py /source/to/pdf --page_start 232 --page_end 254

----------------------------

Parameters:
--page_start [(0,Infinity)]
  Starting page, defaults to 0

--page_end [(0,Infinity)]
  Ending page, defaults to end of document

--paragraph_start [(0,Infinity)]
  Starting paragraph, defaults to 0, the first paragraph

--paragraph_end [(0,Infinity)]
  Ending paragraph, defaults to end of page

----------------------------
  
Optionals:
--unique:
  [FLAG] Determines wether to return all links only once
"""

import argparse
import logging
import os
import re
from ast import Dict
from concurrent.futures import ThreadPoolExecutor
from sys import maxsize
from typing import Callable, List

from pypdf import PageObject, PdfReader

PARAGRAPH_DELIMITER = "\n\n"
INFINITY = maxsize


def get_cli_args():
    """Returns the CLI args"""
    parser = argparse.ArgumentParser(
        prog='get_words_from_pdf',
        description='Gets the words from a PDF and applies some operations to them',
        epilog='Developed by Pepe Fabra Valverde'
    )

    # path
    parser.add_argument('filename',
                        help="Absolute path to the PDF")

    # parameters
    parser.add_argument('--page_start', type=int,
                        help="Start reading since this page", default=0)
    parser.add_argument('--page_end', type=int,
                        help="Stop reading since at this page", default=INFINITY)
    parser.add_argument('--paragraph_start', type=int,
                        help="Start reading since this paragraph", default=0)
    parser.add_argument('--paragraph_end', type=int,
                        help="Stop reading since at this paragraph", default=INFINITY)

    # optional "flags"
    parser.add_argument('-u', '--unique', action='store_true',
                        help="Determines wether to return all links only once",
                        default=False, required=False)

    args = parser.parse_args()

    return {
        "filename": args.filename,
        "page_start": args.page_start,
        "page_end": args.page_end,
        "paragraph_start": args.paragraph_start,
        "paragraph_end": args.paragraph_end,
        "unique": args.unique
    }


def get_pdf(filename: str) -> PdfReader:
    """Returns the PdfReader instance, or raises an error"""
    if not os.path.exists(os.path.realpath(filename)):
        raise FileNotFoundError("File not found in the system")

    return PdfReader(filename)


def get_pages(pdf_instance: PdfReader, page_start: int, page_end: int) -> List[PageObject]:
    """Gets the pages by range"""
    if len(pdf_instance.pages) <= 0:
        raise ValueError("Empty content, no pages were found in the PDF")

    return [
        page
        for index, page in enumerate(pdf_instance.pages)
        if page_start <= index <= page_end
    ]


def subtract_text(
    pages: List[PageObject],
    paragraph_start: int,
    paragraph_end: int,
    on_page_read: Callable[[str], None],
) -> None:
    """Gets the text from the pages, might use a concurrency/parallelism technique"""
    # evaluate first paragraph clause
    on_page_read(
        PARAGRAPH_DELIMITER.join(
            pages[0]
            .extract_text()
            .split(PARAGRAPH_DELIMITER)[paragraph_start:]
        )
    )

    # evaluate the rest
    with ThreadPoolExecutor() as executor:
        executor.map(
            lambda page: on_page_read(page.extract_text()),
            pages[1:-1],
        )

    # evaluate last paragraph clause
    on_page_read(
        PARAGRAPH_DELIMITER.join(
            pages[-1]
            .extract_text()
            .split(PARAGRAPH_DELIMITER)[:paragraph_end]
        )
    )


def get_hyperlinks_from_text(text: str) -> List[str]:
    """Retrieves all the hyperlinks from a text"""
    return re.findall(r"(https?://\S+)", text)


def get_hyperlinks(
    pages: List[PageObject],
    paragraph_start: int = 0,
    paragraph_end: int = INFINITY,
    unique: bool = False
) -> List[str]:
    """Returns all the hyperlinks"""
    hyperlinks: List[str] = []

    subtract_text(
        pages,
        paragraph_start,
        paragraph_end,
        on_page_read=lambda x: hyperlinks.extend(
            get_hyperlinks_from_text(x)
        )
    )

    if unique:
        hyperlinks = list(set(hyperlinks))

    return hyperlinks


def prepare(cli_args: Dict) -> None:
    """Prepares the system"""
    logger = logging.getLogger("pypdf")
    logger.setLevel(logging.ERROR)

    assert cli_args["filename"].endswith(".pdf")
    assert cli_args["page_start"] <= cli_args["page_end"]

    if cli_args["page_start"] == cli_args["page_end"]:
        assert cli_args["paragraph_start"] <= cli_args["paragraph_end"]


def entrypoint() -> None:
    """Entrypoint"""
    cli_args = get_cli_args()
    prepare(cli_args)

    pdf_instance = get_pdf(cli_args["filename"])

    pages = get_pages(
        pdf_instance,
        cli_args["page_start"],
        cli_args["page_end"]
    )

    hyperlinks = get_hyperlinks(
        pages,
        cli_args["paragraph_start"],
        cli_args["paragraph_end"],
        unique=cli_args["unique"]
    )

    print(hyperlinks)


if __name__ == "__main__":
    entrypoint()
