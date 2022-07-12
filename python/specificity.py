# Typing
from typing import List, Tuple
# Regex
import re
# List utilities
from functools import reduce


def get_rule_points(
    rule: str
) -> int:
    """
    Gets the points from a rule

    rule : str
        The rule to evaluate

    returns number The number of points of that CSS selector
    """
    if not rule:
        return 0

    first_character = rule[0]

    if first_character == ".":
        # classes
        return 10
    elif first_character == "#":
        # ids
        return 100
    elif re.match(r'[a-z]', first_character, re.IGNORECASE):
        # html tags
        return 1

    return 0


def get_specificity_points(
    instruction: str
) -> int:
    """
    Calculates the points of a CSS instruction

    instruction : str
        The CSS instruction to evaluate

    returns number The total points
    """
    selectors = instruction.split(" ")
    points = reduce(
        lambda prev, curr: prev + get_rule_points(curr),
        selectors,
        0
    )
    return points


def evaluate_css_rules(
    rules: List[str],
    ascending: bool = False,
    with_scores=True,
) -> List[Tuple[str, int]]:
    """
    Evaluates multiple CSS rules and sorts them

    rules : List[str]
        The rules to evaluate
    ascending : bool
        If it will be ascending, it won't by default
    with_scores : bool
        Will it return the scores, it will by default

    returns List[Tuple[str, int]]
    """
    rules_with_specificity = map(
        lambda rule: (rule, get_specificity_points(rule)),
        rules
    )
    sorted_rules = sorted(
        rules_with_specificity,
        key=lambda x: x[1],
        reverse=not ascending
    )

    if not with_scores:
        sorted_rules = map(lambda rule, _: rule, sorted_rules)

    return sorted_rules


# checkout my css specificity calculator for a more interactive utility
# https://github.com/jofaval/css-specificity-calculator
if __name__ == '__main__':
    # should evaluate them all together
    assert evaluate_css_rules(
        rules=[
            "my-lonely-html-tag",
            "#unique-id > .my-class + my-cool-html-tag",
        ]
    ) == [
        ("#unique-id > .my-class + my-cool-html-tag", 111),
        ("my-lonely-html-tag", 1),
    ]
