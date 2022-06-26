import re
from typing import Callable, List

"""
# CHANGELOG #

## 2022-01-04
### Added
- Project started because of:
  - https://twitter.com/MrRichi94/status/1478367534147645446
  - https://twitter.com/SaraaDeop/status/1478340161243074560
- Succesfull execution at, at least, 15:37, most likely sooner
- Implemented reverse parsing (conversion), successfully tested at 15:52
- Implement basic unit test cases and successfully passed them all at 15:58
"""

def translate(values: list, translator: Callable[[str,], str]) -> List[str]:
    """
    Translate some values given a translator

    values : list
        The values to translate
    translator : Callable[[str,], str]
        The callable lambda that actually translates

    returns List[str]
    """
    translated = [ translator(value) for value in values ]

    return translated

def convert_ascii_to_text(codes: List[str]) -> str:
    """
    Converts ascii codes to text

    codes : List[str]
        The array of ascii codes to covert to text
    
    returns str
    """
    translator = lambda code: chr(int(code))

    return translate(codes, translator)

def convert_text_to_ascii(codes: List[str]) -> str:
    """
    Converts text to ascii codes

    codes : List[str]
        The array of text to covert to ascii codes
    
    returns str
    """
    translator = lambda code: ord(str(code))

    result = translate(codes, translator)

    # Parse them to string
    result = [ str(code) for code in result ]

    return result

def convert_binary_to_ascii(binaries: List[str], base: int = 2) -> List[str]:
    """
    Converts binary codes to ascii codes

    binaries : List[str]
        The binaries to parse
    base : int
        The number base to use, two by default

    returns List[str]
    """
    translator = lambda code: int(code, base)

    return translate(binaries, translator)

def convert_ascii_to_binary(codes: List[str]) -> List[int]:
    """
    Converts ascii codes to binary codes

    codes : List[str]
        The ascii to parse

    returns List[str]
    """
    translator = lambda code: bin(int(code))

    result = translate(codes, translator)
    
    # Clean the input
    result = [ str(char).replace('0b', '') for char in result ]

    return result

def get_user_input(prompt: str = 'El texto a parsear: ') -> str:
    """
    Gets the user input

    prompt : str
        The input prompt

    returns str
    """
    text = input(prompt)
    text = text.strip()

    return text


def parse_input(delimiter: str = '\s') -> str:
    """
    Gets the user input and parses it to text

    delimiter : str
        The delimiter to use

    returns str
    """
    # Get the user input
    text = get_user_input()
    # Split the user input, to get the character codes only
    splitted = re.compile(delimiter).split(text)

    # The raw ASCII codes to text values
    parsed = convert_ascii_to_text(splitted)

    # The joined parsed ASCII characters
    joined = ''.join(parsed)

    return joined

def convert_input() -> str:
    """
    Gets the user input and converts it to binary

    returns str
    """

    # Get the user input
    text = get_user_input('El texto a convertir: ')
    # Split the user input, to get the character codes only
    splitted = text

    # The raw ASCII codes to text values
    parsed = convert_text_to_ascii(splitted)
    # parsed = convert_ascii_to_binary(parsed)

    # The joined parsed ASCII characters
    joined = ' '.join(parsed)

    return joined

def main() -> None:
    """
    Holds the main workflow execution

    returns None
    """
    # result = parse_input()
    result = convert_input()

    print(f'El resultado ha sido: "{result}"')

def test() -> None:
    """
    Creates the unit test cases

    returns None
    """
    assert convert_text_to_ascii('Proximamente') == [
        '80', '114', '111', '120', '105', '109', '97', '109', '101', '110', '116', '101'
    ]
    assert convert_ascii_to_text([
        '80', '114', '111', '120', '105', '109', '97', '109', '101', '110', '116', '101'
    ]) == list('Proximamente')

if __name__ == '__main__':
    test()
    main()