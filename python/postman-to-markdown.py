import argparse
from os.path import exists
from json import dumps, load, loads
from re import sub
from typing import List


def get_args_parser() -> argparse.ArgumentParser:
    """
    Initializes the parser

    @source=https://stackoverflow.com/questions/40001892/reading-named-command-arguments

    returns argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--collection', help="""
    The Postman Collection to parse.
    A complete absolute path should be given.
    Currently only working with the latest exported version (v2.1)
    """)
    parser.add_argument('--destination', help="""
    The wanted destination file.
    A complete absolute path should be given.
    """)

    return parser


def get_collection_content(
    collection_source: str
) -> dict:
    """
    Gets the parsed content from the given collection

    collection_source : str
        The absolute path to the collection

    returns dict
    """
    assert exists(collection_source)

    content = None
    with open(collection_source) as reader:
        content = load(reader)
    return content


def get_collection_title(
    collection: dict
) -> str:
    """
    Get the title from the given collection

    collection: dict
        The collection to evaluate

    returns str
    """
    return f"# {collection['info']['name']} #"


def get_slugified_name(
    name: str
) -> str:
    """
    Gets the slugified version of a given item name

    name : str
        The given item name

    returns str
    """
    slug = name.lower()
    slug = sub(r'\s+', '-', slug)
    slug = sub(r'[\/\[\]\.]', '', slug)
    slug = sub(r'\-+', '-', slug)

    return slug


def get_collection_table_of_contents(
    collection: dict
) -> List[str]:
    """
    Get the table scheme of contents from the given collection

    collection: dict
        The collection to evaluate

    returns List[str]
    """
    contents = []
    for item in collection['item']:
        contents.append(
            f"1. [{item['name']}](#{get_slugified_name(item['name'])})")
        if 'item' in item:
            sub_elements = get_collection_table_of_contents(item)
            sub_elements = [
                contents.append(f"\t{element}")
                for element in sub_elements
            ]

    return contents


def get_query_markdown_table(
    request_details: dict
) -> str:
    """
    Generates a markdown table from a collection's request's details, if possible

    request_details : dict
        The collection's request's details

    returns str
    """
    if 'query' not in request_details['url'] or len(request_details['url']['query']) < 1:
        return 'This request does not have any query params available, or documented.'

    query_params = request_details['url']['query']
    markdown_table = []

    markdown_table.append('**HTTP query params**')
    markdown_table.append('')
    markdown_table.append(
        f"| {' | '.join([ f'**{colname}**' for colname in query_params[0].keys() ])} |")
    markdown_table.append(
        f"| {' | '.join([ '---' for _ in query_params[0].keys() ])} |")
    for query_param in query_params:
        try:
            def get_value(key, value):
                if value is None:
                    value = ''
                return f'**{value}**' if key in ['key'] else value
            markdown_table.append(
                f"| {' | '.join([ get_value(key, value) for key, value in query_param.items() ])} |"
            )
        except:
            print(query_param)
    markdown_table = '\n'.join(markdown_table)

    return markdown_table


def get_request_body(
    request_details: dict,
    body_type: str = 'raw',
) -> str:
    """
    Generates a markdown json body from a collection's request's body, if possible

    request_details : dict
        The collection's request's details
    body_type : str
        The body's type, it will always try to be raw

    returns str
    """
    if 'body' not in request_details or not request_details['body']:
        return 'This request does not have an example request body.'

    body_details = request_details['body']
    body_lang = body_details['options'][body_type]['language']

    body = body_details[body_type]
    # body = sub(r'[\s]+', ' ', body)
    # body = sub(r'(\\r\\n)+', '\n', body)
    try:
        body = dumps(loads(body), indent=4)
    except:
        # print(body)
        return 'This request does not have an example request body.'

    return '\n'.join([
        '<details>',
        "<summary>Show request's body</summary>",
        '  ',
        f"```{body_lang}\n{body}\n```",
        '</details>',
    ])


def parse_collection_item_to_markdown(
    item: dict,
    recursive_level: int = 3,
    parent: dict = None,
) -> str:
    """
    Parses a collection item to markdown

    item : dict
        The collection's item to parse
    recursive_level : int
        The index level for the markdown titles
    parent : dict
        The parent of this element

    returns str
    """
    request_details = item['request']

    item_details = [
        '\n'.join([
            f"{recursive_level * '#'} {item['name']}",
            f"[Back to {parent['name']}](#{get_slugified_name(parent['name'])})",
        ]),
        '\\\n'.join([
            f"**HTTP method**: {request_details['method'] if 'method' in request_details else 'none to be kown.'}",
            f"**Authentication type**: {request_details['auth']['type'] if 'auth' in request_details else 'none to be kown.'}",
            f"**Url**: `{request_details['url']['raw'] if request_details['url']['raw'] else 'none to be found.'}`"
        ]),
        f"Description: {request_details['description'] if 'description' in request_details else 'None.'}",
        get_query_markdown_table(request_details),
        get_request_body(request_details)
    ]

    return '\n\n'.join(item_details)


def get_parsed_collection_items(
    collection: dict,
    recursive_level: int = 2,
    parent: dict = None,
) -> List[str]:
    """
    Gets the parsed collection items, the body you could say

    collection : dict
        The parsed collection's content
    recursive_level : int
        The index level for the markdown titles
    parent : dict
        The parent of this element

    returns List[str]
    """
    assert 'item' in collection

    contents = []

    for item in collection['item']:
        if 'item' in item:  # is a folder
            contents.append('\n'.join([
                f"{recursive_level * '#'} {item['name']}",
                f"[Back to {parent['name']}](#{get_slugified_name(parent['name'])})"
            ]))
            if 'description' in item:
                contents.append(item['description'])
            # table of contents here
            contents.append(
                get_parsed_collection_items(
                    item,
                    recursive_level=recursive_level + 1,
                    parent=item
                )
            )
        else:  # it's an element (most likely a request)
            contents.append(parse_collection_item_to_markdown(
                item,
                recursive_level,
                parent=parent,
            ))

    return '\n\n'.join(contents)


def get_with_variables_replaced(
    markdown: str,
    collection: dict,
) -> str:
    """
    Replaces the variables so that the document is more readable,
    as readable as possible without overengineering.

    markdown : str
        The raw generated markdown document
    collection : dict
        The parsed collection's content

    returns str
    """
    parametrized_markdown = markdown

    copied_variables = collection['variable']
    for variable in copied_variables:
        key, value = variable['key'], variable['value']
        parametrized_markdown = parametrized_markdown.replace(
            '{{' + key + '}}',
            value,
        )

    return parametrized_markdown


def get_markdown_from_collection(
    collection: dict,
    credit_repository=True,
) -> str:
    """
    Generate/extract the markdown content from the collection's dict

    collection : dict
        The parsed collection's content

    returns str
    """
    markdown = []

    markdown.append(get_collection_title(collection))

    if credit_repository:
        repository = 'https://github.com/jofaval/utilities'
        filepath = f'{repository}/blob/master/python/postman-to-markdown.py'
        markdown.append(f'Generated with [{filepath}]({filepath})')

    markdown.append('## Contents')
    markdown.append('\n'.join(get_collection_table_of_contents(collection)))
    markdown.append(get_parsed_collection_items(
        collection, parent={'name': 'Contents'}))

    parsed_markdown = '\n\n'.join(markdown)
    parsed_markdown = parsed_markdown.replace('\[', '[')
    parsed_markdown = parsed_markdown.replace('\]', ']')

    parsed_markdown = get_with_variables_replaced(parsed_markdown, collection)

    return parsed_markdown


def save_mardown(
    markdown: str,
    destination: str,
) -> int:
    """
    Saves the markdown in the required file

    markdown : str
        The markdown to save
    destination : str
        The file it will be saved in

    returns int
    """
    success = 0
    with open(destination, 'w+') as writer:
        success = writer.write(markdown)
    return success


def main() -> None:
    """
    Initializes the workflow

    returns None
    """
    args = get_args_parser().parse_args()

    collection = get_collection_content(args.collection)
    markdown = get_markdown_from_collection(collection)
    # print(markdown)

    success = save_mardown(markdown, destination=args.destination)


if __name__ == '__main__':
    main()

    # Collection
    # "D:/Pepe/WebDesign/xampp/htdocs/e-learning/[Go(lang)] E-Learning.postman_collection.json"
    # Destination
    # "D:/Pepe/WebDesign/xampp/htdocs/utilities/ignore/python/postman-to-markdown/[Go(lang)] E-Learning.postman_collection.md"
