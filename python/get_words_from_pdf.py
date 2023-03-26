"""
Get the words from a PDF

python3 get_words_from_pdf.py /source/to/pdf

----------------------------

Example:
python3 get_words_from_pdf.py /source/to/pdf --page_start 232 --page_end 254

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
--length:
  [FLAG] Retrieves the total number of words, accumulative
  
--read_time [optional words_per_minute]:
  [FLAG] Retrieves the total number of read time (given words_per_minute), accumulative
"""

import argparse
import os
import re
from sys import maxsize
from typing import List

from pypdf import PdfReader

# Source: https://irisreading.com/what-is-the-average-reading-speed/
AVG_LEARNING_RATE_WORDS_PER_MINUTE = 150
AVG_COMPREHENSION_RATE_WORDS_PER_MINUTE = 300
AVERAGE_WORDS_PER_MINUTE = AVG_LEARNING_RATE_WORDS_PER_MINUTE

PARAGRAPH_SEPARATOR = "\n\n"
INFINITY = maxsize


def get_total_words(text: str) -> List[str]:
    """Given a text, returns the total amount of words"""
    total_words = re.findall(r"\w+", text)

    print("Total words found:", len(total_words), "word(s) found.")

    return total_words


def get_total_read_time(total_words: int, words_per_minute: int = AVERAGE_WORDS_PER_MINUTE) -> int:
    """Given the total words and words_per_minutes, returns the total read time for those words"""
    if not isinstance(words_per_minute, int):
        words_per_minute = AVERAGE_WORDS_PER_MINUTE
    return round(total_words / words_per_minute)


def parse_pdf_page_text(text: str, paragraph_start: int, paragraph_end: int) -> str:
    """Parses a PDF page to get the desired amount of paragraphs"""
    paragraphs = text.split(rf"/{PARAGRAPH_SEPARATOR}+/")
    if not paragraphs or len(paragraphs) <= 0:
        return ""

    return PARAGRAPH_SEPARATOR.join(paragraphs[paragraph_start:paragraph_end])


def get_pdf_text(
    pdf_path: str,
    page_start: int = 0,
    page_end: int = INFINITY,
    paragraph_start: int = 0,
    paragraph_end: int = INFINITY
) -> str:
    """Gets the text from a PDF given certain constraints"""
    assert pdf_path.endswith(".pdf")

    reader = PdfReader(pdf_path)
    text = [
        parse_pdf_page_text(
            page.extract_text(),
            paragraph_start,
            paragraph_end
        )
        for (index, page) in enumerate(reader.pages)
        if page_start <= index <= page_end
    ]
    print(len(text), "page(s) extracted.")
    text = "\n".join(text)

    return text


def get_cli_args():
    """Retrieves the CLI args"""
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
    parser.add_argument('-l', '--length', type=bool,
                        help="Retrieve the total amount of words",
                        default=True)
    parser.add_argument('-r', '--read_time', type=int,
                        help="Average word per minute read time (learning rate at ~150 words/minute)",
                        default=AVERAGE_WORDS_PER_MINUTE)

    args = parser.parse_args()

    return {
        "pdf_path": os.path.realpath(args.filename),
        "page_start": args.page_start,
        "page_end": args.page_end,
        "paragraph_start": args.paragraph_start,
        "paragraph_end": args.paragraph_end,
        "length_flag": args.length,
        "read_time_flag": args.read_time,
    }


def entrypoint() -> None:
    """Entrypoint"""
    cli_args = get_cli_args()

    pdf_text = get_pdf_text(
        pdf_path=cli_args["pdf_path"],
        page_start=cli_args["page_start"],
        page_end=cli_args["page_end"],
        paragraph_start=cli_args["paragraph_start"],
        paragraph_end=cli_args["paragraph_end"],
    )

    total_words = False
    if cli_args["length_flag"]:
        total_words = len(get_total_words(pdf_text))

    if cli_args["read_time_flag"]:
        if not total_words:
            total_words = get_total_words(pdf_text)

        total_read_time = get_total_read_time(
            total_words, cli_args["read_time_flag"]
        )
        total_read_time_in_hours = round(total_read_time / 60)

        print(
            "Total read time for", total_words, "word(s) is around",
            total_read_time, "minute(s), or",
            total_read_time_in_hours, "hour(s)."
        )


if __name__ == "__main__":
    entrypoint()
