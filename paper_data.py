import json
from typing import List, Optional

from dataclasses import dataclass, asdict
import reference

@dataclass
class MainSection:
    title: str
    beginning: str
    ref_entries: List[str]

    final_content: str

@dataclass(init=False)
class PaperData:
    title: str
    addition_tldr: str
    abstract: str
    introduction_section: str
    main_sections: List[MainSection]

    def __init__(self, title, addition_tldr, main_sections, abstract = '', introduction_section = '') -> None:
        self.title = title
        self.addition_tldr = addition_tldr
        self.abstract = abstract
        self.introduction_section = introduction_section
        if len(main_sections) and isinstance(main_sections[0], dict):
            self.main_sections = [MainSection(**section) for section in main_sections]
        else:
            self.main_sections = main_sections

    def save(self, path):
        with open(path, 'w') as f:
            json.dump(asdict(self), f, indent=2)

    @classmethod
    def load(cls, path):
        with open(path) as f:
            data = json.load(f)
        return cls(**data)
