import re
from typing import List, Match, Pattern

from ._syntax import _patterns, _priority


def _strip_tags(source: str) -> str:
    return re.sub(r"</?[^>]+>", "", source)


def _strip_default(patterns: List[Pattern], source: str) -> str:
    def replacement(match: Match) -> str:
        # extra whitespaces will be removed
        return " {text} ".format(text=match.groupdict().get("text", ""))

    for pattern in patterns:
        source = pattern.sub(replacement, source)

    return source


def _strip_macro(patterns: List[Pattern], source: str) -> str:
    for pattern in patterns:
        source = pattern.sub(r" ", source)

    return source


def _strip_html(patterns: List[Pattern], source: str) -> str:
    def replacement(match: Match) -> str:
        return _strip_tags(match.group("text"))

    for pattern in patterns:
        source = pattern.sub(replacement, source)

    return source


def _strip_inline(patterns: List[Pattern], source: str) -> str:
    def replacement(match: Match) -> str:
        # extra whitespaces will be removed
        return match.groupdict().get("text", "")

    for pattern in patterns:
        source = pattern.sub(replacement, source)

    return source


_strip_link = _strip_inline
_strip_bold = _strip_inline
_strip_italic = _strip_inline
_strip_underline = _strip_inline
_strip_superscript = _strip_inline
_strip_subscript = _strip_inline
_strip_text_size = _strip_inline
_strip_text_color = _strip_inline


def _strip_deletion(patterns: List[Pattern], source: str) -> str:
    items = []

    def replacement(match: Match) -> str:
        items.append(match.group("text"))
        return ""

    for pattern in patterns:
        source = pattern.sub(replacement, source)

    if items:
        source += "\n"
        source += "\n".join(items)

    return source


def _strip_footnote(patterns: List[Pattern], source: str) -> str:
    def _do_strip_footnote(source: str):
        items = []

        def replacement(match: Match) -> str:
            items.append(match.groupdict().get("text", ""))
            return ""

        for pattern in patterns:
            source = pattern.sub(replacement, source)

        if items:
            source += "\n"
            source += "\n".join(items)

        return source

    # to handle nested footnotes
    previous_source = None
    while previous_source != source:
        previous_source = source
        source = _do_strip_footnote(source)

    return source


def _clean_whitespace(source: str) -> str:
    # strip whitespaces line by line
    source = re.sub(r"^[ \t]*(.*?)[ \t]*$", r"\1", source, flags=re.MULTILINE)

    # remove duplicated whitespaces
    source = re.sub(r"(\s)\1+", r"\1", source)

    return source.strip()


def extract_text(source: str) -> str:
    environment = globals()

    for item in _priority:
        name = "_strip_{item}".format(item=item)
        strip = _strip_default if name not in environment else environment[name]

        source = strip(_patterns[item], source)

    return _clean_whitespace(source)
