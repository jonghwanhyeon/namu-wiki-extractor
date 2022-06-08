import re

_patterns = {
    'macro': [
        r'\[\[(?P<name>date|datetime|br|include|목차|tableofcontents|각주|footnote|pagecount|youtube|nicovideo|wikicommons)(?:\(.+?\))?\]\]', # rigvedawiki syntax
        r'\[(?P<name>date|datetime|br|include|목차|tableofcontents|각주|footnote|pagecount|youtube)(?:\(.+?\))?\]',
        r'\[\[(?P<name>분류)\:.*?\]\]',# acts like macro
    ],

    'html': [
        r'\{\{\{\#\!html[ \t\n]*(?P<text>[\s\S]*?)\}\}\}',
        r'\[\[html[ \t]*\((?P<text>[^\)]*)\)\]\]', # rigvedawiki syntax
    ],

    'image': [
        r'\[\[파일\:[ \t]*.*?\.(?:jpg|jpeg|png|gif)(?:\|[\&a-z\=\d\%]*)?\]\]',
        r'(?:https?|ftp).*?\.(?:jpg|jpeg|png|gif)(?:[\?\&a-z\=\d\%]*)?',
        r'attachment\:[ \t]*[\"\']?.*?\.(?:jpg|jpeg|png|gif)(?:[\?\&a-z\=\d\%]*)?[\"\']?', # rigvedawiki syntax
    ],

    'link': [
        # [[문서|출력]]
        r'\[\[[^\|\]]*\|(?P<text>[^\]]*)\]\]',
        # [[\#문서]]
        r'\[\[\\(?P<text>\#[^\]]*?)(?:\#[^\]]*)?\]\]',
        # [[문서#s-2.3]]
        r'\[\[(?P<text>[^\#][^\]]*?)(?:\#[^\]]*)?\]\]',
        # [[#s-1]]
        r'\[\[\#(?P<text>[^\]]*)\]\]', 
    ],

    'horizontal_rule': r'-{4,10}',
    'heading': r'={1,}[ \t]+(?P<text>.*?)[ \t]+\={1,}',
    
    'bold': r"'''(?P<text>.*?)'''",
    'italic': r"''(?P<text>.*?)''",
    'deletion': r'(~~~|~~|--)(?P<text>.*?)\1',
    'underline': r'__(?P<text>.*?)__',
    'superscript': r'\^\^(?P<text>.*?)\^\^',
    'subscript': r',,(?P<text>.*?),,',
    'text_size': r'\{\{\{\+\d+[ \t]+(?P<text>.*?)\}\}\}',
    'text_color': r'\{\{\{\#(?:[0-9a-f]+|[a-z]+)[ \t]+(?P<text>.*?)\}\}\}',

    'math': [
        r'<math>.*?</math>',
        r'\$.*?\$', # rigvedawiki syntax
    ],

    'text_box': r'\{\{\|(?P<text>[\s\S]*?)\|\}\}',
    'table': r'\|.*?\|(?:<[^>]*>)*(?P<text>[^\|]*)',

    'unordered_list': r'^[ \t]+\*[ \t]*(?P<text>.*)$',
    'ordered_list': r'^[ \t]+[1AaIi]\.[ \t]*(?:\#\d+)?[ \t]*(?P<text>.*)$',
    'quote': r'\>+[ \t]*(?P<text>.*)',

    'syntax': r'\{\{\{\#\!syntax[ \t\n]+[\s\S]*?\}\}\}',
    'wiki': r'\{\{\{\#\!wiki[ \t\n]+style[ \t]*\=[ \t]*\".*?\"[ \t]*(?P<text>[\s\S]*?)\}\}\}',
    'folding': r'\{\{\{\#\!folding[ \t\n]+(?P<text>[\s\S]*?)\}\}\}', # rigvedawiki syntax
    'plaintext': r'\{\{\{(?P<text>[\s\S]*?)\}\}\}',

    'comment': r'\#\#.*',
    'redirect': r'\#(?:redirect|넘겨주기)[ \t\n]+.*',

    'footnote': [
        r'\[\*[^ \t]+\]', 
        r'\[\*[^ \t]*[ \t]+(?P<text>[^\[\]]*)\]',
    ],
}

_priority = (
    'macro',
    'html', # before link
    'image', # before link 
    'link',
    'horizontal_rule', # before deletion
    'heading',
    'bold',
    'italic', # after bold
    'deletion',
    'underline',
    'superscript',
    'subscript',
    'text_size',
    'text_color',
    'math',
    'text_box', # before table
    'table', # before list
    'unordered_list',
    'ordered_list', 
    'quote',
    'syntax',
    'wiki',
    'folding',
    'plaintext', # after text_size, text_color, html, syntax, wiki, and folding
    'comment',
    'redirect',
    'footnote',
)

# compile regular expressions
for name in _patterns:
    if not isinstance(_patterns[name], list):
        _patterns[name] = [ _patterns[name] ] 

    _patterns[name] = [
        re.compile(pattern, re.IGNORECASE | re.MULTILINE)
        for pattern in _patterns[name]
    ]