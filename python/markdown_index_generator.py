"""
Defines table of contents start: <-- [toc-start] -->
Defines table of contents end: <-- [toc-end] -->
Ignore with: <-- [ignore] -->
"""

from typing import List, Optional

from pydantic import BaseModel

IGNORE_SECTION = "<-- [ignore] -->"
TABLE_OF_CONTENTS_START = "<-- [toc-start] -->"
TABLE_OF_CONTENTS_END = "<-- [toc-end] -->"


class MarkdownEntry(BaseModel):
    """Markdown entry details, DAO"""
    id: int
    level: int
    title: str
    children: Optional["List[MarkdownEntry]"]


class MarkdownTableOfContentsOptions(BaseModel):
    # TODO: implement and actually put it to use
    """Configuration details for the table of contents generation"""
    indent_level: int = 0
    """How much detail is wanted"""
    ordered_list: bool = True
    """Will the level indicator be numeric, or symbols"""


def get_args() -> dict:
    """Parses the cli args"""
    args = {}
    raise NotImplementedError("get_args")
    return args


def get_file_contents(file: str) -> str:
    """Retrieves the markdown file content, if any"""
    contents = ""
    raise NotImplementedError("get_file_contents")
    return contents


def is_markdown_file_valid(contents: str) -> bool:
    """
    Checks for the necessary opening and closing region tags

    Defines table of contents start: <-- [toc-start] -->
    Defines table of contents end: <-- [toc-end] -->
    Ignore with: <-- [ignore] -->
    """
    is_valid = True
    raise NotImplementedError("is_markdown_file_valid")
    return is_valid


def get_markdown_details(contents: str) -> List[MarkdownEntry]:
    """Generates a list of markdown entries so that they can be sorted late"""
    raise NotImplementedError("get_markdown_details")


def get_nested_markdown_details(entries: List[MarkdownEntry]) -> List[MarkdownEntry]:
    """From a list of markdown entries, gets the actually sorted and nested version"""
    raise NotImplementedError("get_nested_markdown_details")


def generate_markdown_table_of_contents(
    entries: List[MarkdownEntry],
    options: MarkdownTableOfContentsOptions = None
) -> str:
    """From the list of entries, generates the table of contents"""
    table_of_contents = ""
    if not options:
        options = MarkdownTableOfContentsOptions()
    raise NotImplementedError("generate_markdown_table_of_contents")
    return table_of_contents


def update_markdown_contents(contents: str, table_of_contents: str) -> str:
    """In-memory operation"""
    raise NotImplementedError("update_markdown_contents")


def write_contents_to_file(file: str, contents: str) -> str:
    """After the content has been generated, it gets saved"""
    raise NotImplementedError("write_contents_to_file")


def main():
    """Entrypoint"""
    # parsing
    args = get_args()
    file_path = args['file']

    # validation
    contents = get_file_contents(file_path)
    if not is_markdown_file_valid(contents):
        raise ValueError("Invalid formatting, TODO: add details")

    # generation
    markdown_details = get_markdown_details(contents)
    nested_markdown_details = get_nested_markdown_details(markdown_details)
    table_of_contents = generate_markdown_table_of_contents(
        nested_markdown_details
    )

    # saving
    new_contents = update_markdown_contents(contents, table_of_contents)
    write_contents_to_file(file_path, new_contents)


if __name__ == "__main__":
    main()
