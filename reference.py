from dataclasses import dataclass, asdict
from typing import Any, List, Dict, Optional
from pybtex.database import parse_string, parse_file
import scipdf
import os
import json

grobid_url = "http://localhost:8070"

@dataclass
class Reference:
    article_type: str
    title: str
    authors: List[str]
    abstract: str
    publication_year: int
    keywords: str
    doi: str

# reference_data = {
#     "title": "Sample Title",
#     "authors": ["Author1", "Author2"],
#     "abstract": "This is a sample abstract.",
#     "publication_year": 2023,
#     "doi": "doi:10.1234/example"
# }

# reference = Reference(**reference_data)

@dataclass
class AIsuggesion:
    relation: str
    suggestion: str
    rating: int

@dataclass(init=False)
class DetailReference:
    base: Reference
    suggestion: Optional[AIsuggesion]
    sections: List[Any]
    def __init__(self, base, suggestion, sections) -> None:
        if isinstance(base, Reference):
            self.base = base
        else:
            self.base = Reference(**base)
        
        if suggestion is None: 
            self.suggestion = None
        elif isinstance(suggestion, AIsuggesion):
            self.suggestion = suggestion
        else:
            self.suggestion = AIsuggesion(**suggestion)

        self.sections = sections

RefsType = Dict[str, DetailReference]

def readbib(bibfile = 'reliAI.bib') -> List[Reference]:
    bibentries = parse_file(bibfile)
    refs = {}
    for ref_entry, paper in bibentries.entries.items():
        try:
            ref = Reference(
                article_type = paper.type,
                title = paper.fields['title'][1:-1],
                doi = paper.fields.get('doi', ''),
                publication_year = paper.fields.get('year', ''),
                keywords = paper.fields.get('keywords', ''),
                abstract = paper.fields['abstract'],
                authors = [str(person) for person in paper.persons['author']]
            )
        except KeyError as e:
            print(f'Error when processing bib item {ref_entry}')
            print('KeyError:', e)
            exit(1)
        refs[ref_entry] = DetailReference(ref, None, None)
    return refs

def matchPDFs(refs: Dict[str, DetailReference], pdf_folder):
    def match_data(title):
        for key, ref in refs.items():
            if ref.base.title == title:
                return key
        
        raise Exception(f'Failed to match paper "{title}"')

    for pdf_file in os.listdir(pdf_folder):
        if pdf_file[-4:]!='.pdf':
            continue
        res = scipdf.parse_pdf_to_dict(pdf_folder + '/' + pdf_file, grobid_url=grobid_url)

        p_title = res['title']

        key = match_data(p_title)
        refs[key].introduction = res['sections'][0]['text']
        
        exit(0)

def loadPDFs(pdf_folder):
    refs = {}
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file[-4:]!='.pdf':
            continue
        print('processing ', pdf_file)
        paper = scipdf.parse_pdf_to_dict(pdf_folder + '/' + pdf_file, grobid_url=grobid_url)

        ref = Reference(
            article_type = paper.type,
            title = paper['title'],
            doi = paper.get('doi', ''),
            publication_year = '',
            keywords = '',
            abstract = paper['abstract'],
            authors = [paper['authors'].split(';').trim()]
        )
        ref_entry = pdf_file[:-4]
        sections = [(sec['heading'], sec['text']) for sec in paper.sections]
        refs[ref_entry] = DetailReference(base = ref, suggestion = None, sections = sections)

        break

    return refs

def saveDetailReference(refs: Dict[str, DetailReference], path):
    with open(path, 'w') as f:
        json.dump({k: asdict(refs[k]) for k in refs}, f, indent=2)

def loadDetailReference(path):
    with open(path) as f:
        ref_dict = json.load(f)
    return {k: DetailReference(**ref_dict[k]) for k in ref_dict}
