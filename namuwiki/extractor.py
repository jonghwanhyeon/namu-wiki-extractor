import re
from dataclasses import dataclass
from typing import Callable, List, Match, Pattern, Union

from . import macros
from ._syntax import _patterns, _priority


@dataclass
class Document:
    text: str
    deletions: List[str]
    footnotes: List[str]


def _apply_patterns(
    patterns: List[Pattern], replacement: Union[str, Callable[[Match], str]], text: str
) -> str:
    for pattern in patterns:
        text = pattern.sub(replacement, text)
    return text


def _strip_tags(source: str) -> str:
    return re.sub(r"</?[^>]+>", "", source)


def _clean_whitespace(source: str) -> str:
    # strip whitespaces line by line
    source = re.sub(r"^[ \t]*(.*?)[ \t]*$", r"\1", source, flags=re.MULTILINE)

    # remove duplicated whitespaces
    source = re.sub(r"(\s)\1+", r"\1", source)

    return source.strip()


def _strip_default(patterns: List[Pattern], document: Document) -> Document:
    def replacement(match: Match) -> str:
        # extra whitespaces will be removed
        return " {text} ".format(text=match.groupdict().get("text", ""))

    document.text = _apply_patterns(patterns, replacement, document.text)
    return document


def _strip_macro(patterns: List[Pattern], document: Document) -> Document:
    def replacement(match: Match) -> str:
        groups = match.groupdict()
        macro = getattr(macros, groups["name"]) if hasattr(macros, groups["name"]) else macros.default
        return macro(groups.get("parameter", ""))

    document.text = _apply_patterns(patterns, replacement, document.text)
    return document


def _strip_html(patterns: List[Pattern], document: Document) -> Document:
    def replacement(match: Match) -> str:
        return _strip_tags(match.group("text"))

    document.text = _apply_patterns(patterns, replacement, document.text)
    return document


def _strip_inline(patterns: List[Pattern], document: Document) -> Document:
    def replacement(match: Match) -> str:
        # extra whitespaces will be removed
        return match.groupdict().get("text", "")

    document.text = _apply_patterns(patterns, replacement, document.text)
    return document


_strip_link = _strip_inline
_strip_bold = _strip_inline
_strip_italic = _strip_inline
_strip_underline = _strip_inline
_strip_superscript = _strip_inline
_strip_subscript = _strip_inline
_strip_text_size = _strip_inline
_strip_text_color = _strip_inline


def _strip_deletion(patterns: List[Pattern], document: Document) -> Document:
    def replacement(match: Match) -> str:
        document.deletions.append(match.group("text"))
        return ""

    document.text = _apply_patterns(patterns, replacement, document.text)
    return document


def _strip_footnote(patterns: List[Pattern], document: Document) -> Document:
    def _do_strip_footnote(text: str) -> str:
        def replacement(match: Match) -> str:
            document.footnotes.append(match.groupdict().get("text", ""))
            return ""

        return _apply_patterns(patterns, replacement, text)

    # to handle nested footnotes
    previous_text = None
    while previous_text != document.text:
        previous_text = document.text
        document.text = _do_strip_footnote(document.text)
    return document


def extract_text(
    source: str, separate_deletions: bool = False, separate_footnotes: bool = False
) -> Union[str, Document]:
    environment = globals()

    document = Document(text=source, deletions=[], footnotes=[])
    for item in _priority:
        name = "_strip_{item}".format(item=item)
        strip = _strip_default if name not in environment else environment[name]

        document = strip(_patterns[item], document)
    document.text = _clean_whitespace(document.text)

    return_as_document = separate_deletions or separate_footnotes
    if separate_deletions:
        document.text += "\n"
        document.text += "\n".join(document.deletions)
        document.deletions = []

    if separate_footnotes:
        document.text += "\n"
        document.text += "\n".join(document.footnotes)
        document.footnotes = []

    return document if return_as_document else document.text
