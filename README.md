# Namu Wiki Extractor
This module strips the namu mark from a namu wiki document and extracts its plain text only.

# Environment
- Python 3

# Usage
## Simple
    import json
    from namuwiki.extractor import extract_text

    with open('namu_wiki.json', 'r', encoding='utf-8') as input_file:
        namu_wiki = json.load(input_file)

    document = namu_wiki[1]
    plain_text = extract_text(document['text'])

## Multiprocessing
    import json
    from multiprocessing import Pool

    from namuwiki.extractor import extract_text

    def work(document):
        return {
            'title': document['title'],
            'content': extract_text(document['text'])
        }

    with open('namu_wiki.json', 'r', encoding='utf-8') as input_file:
        namu_wiki = json.load(input_file)

    with Pool() as pool:
        documents = pool.map(work, namu_wiki)