# Namu Wiki Extractor
This library strips all [namu marks](https://namu.wiki/w/나무위키:문법%20도움말) from a namu wiki document and extracts its plain text only.

## Requirement
- Python 3

## Installation
```bash
pip install namu-wiki-extractor
```

## Usage
### Basic
```python
import json
from namuwiki.extractor import extract_text

with open('namu_wiki.json', 'r', encoding='utf-8') as input_file:
    namu_wiki = json.load(input_file)

document = namu_wiki[1]
plain_text = extract_text(document['text'])
```

### Multiprocessing
```python
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
```

## API
### namuwiki.extractor.extract_text(source)
Strips all namu marks from `source` and extracts its plain text only. Returns extracted plain text.

#### Parameter
- `source`: text from a namu wiki document

## Note
A JSON dump file of namu wiki can be downloaded from [here](https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4:%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%20%EB%8D%A4%ED%94%84)
