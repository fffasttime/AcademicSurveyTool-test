from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.callbacks import get_openai_callback
from typing import Dict

import reference
import json
import re
import os

from paper_data import PaperData
from utils import dump

# "If you think rating<=3, it's OK to directly use "not relevant" to simply answer the relation and suggestions field. "
read_system_prompt = """
You are an academic literature review helper and now need to read some reference papers to find the necessary information.
User want to write a literature review titled "{title}"{addition_tldr}. Therefore, user will give you a list of title and abstract of papers. Please help determine if the propose of each paper is related to the user's topic, and provide a relation summary and suggestions for citing it. Your response should ONLY include 4 lines for each paper: ID, Relation, Suggestion, Relevance rating. The requirement of each line is:
ID: Input paper ID.
Relation: 1-2 sentences, should not simply including the key points from the original paper, but the purpose and content of the paper related to the user's literature review "{title}".
Suggestion: In one sentence, how to use this paper for review.
Relevance rating: There is only one integer ranging from 1 to 9, the larger the value, the more recommended it is for citation. For example, 6 indicates that it is somehow related, has same purpose as user's review and can be referenced; 3 indicates that there is cross content but different purposes, so it is not recommended.
User's inputs are title and abstract of some paper. For user input format instance:
ID: 1
Title: Paper 1
Abstract: Abstract 1
---
ID: 2
Title: Paper 2
Abstract: Abstract 2
---
Your output should follow the input order, and separated by a --- line after each paper. For output format instance:
ID: 1
Relation: Relation of 1.
Suggestion: Suggestion of 1.
Relevance rating: Relevance rating of 1.
---
ID: 2
Relation: Relation of 2.
Suggestion: Suggestion of 2.
Relevance rating: Relevance rating of 2.
---
"""

read_user_prompt = """
Title: {paper_title}
Full Text:
{paper_text}
"""
read_abstract_user_prompt = """
ID: {ref_id}
Title: {ref_title}
Abstract: {ref_abstract}
"""

def parse_AI_suggestion(output: str):
    relation = re.search('^\s*[Rr]elation\s*:\s*(.*)$', output, re.M)
    suggestion = re.search('^\s*[Ss]uggestions?\s*:\s*(.*)$', output, re.M)
    rating = re.search('^\s*(?:[Rr]elevance)?\s*[Rr]ating\s*:\s*(.*)$', output, re.M)
    if relation is None or suggestion is None or rating is None:
        raise ValueError(f"It seems that AI output has syntax error. Output:\n{output}")
    return reference.AIsuggesion(relation.group(1), suggestion.group(1), int(rating.group(1)))

def preread_abstract(paper_data: PaperData, bibfile, model):
    """
    Batched abstracts reading and write an relevant.
    """
    ref_path = bibfile[:-4] + '_ref.json'
    if os.path.exists(ref_path):
        print(f"{ref_path} already exist, skipping preread_abstract")
        refs = reference.loadDetailReference(ref_path)
        return refs
    else:
        input(f"Enter to preread_abstract from {bibfile}")

    refs: Dict[str, reference.DetailReference] = reference.readbib(bibfile)

    batch_size = 8
    system_template = PromptTemplate.from_template(read_system_prompt)
    system_messsage = system_template.format(title = paper_data.title, addition_tldr = paper_data.addition_tldr)
    literature_template = PromptTemplate.from_template(read_abstract_user_prompt)

    for i in range(0, len(refs), batch_size):
        literature_prompts = []
        literatures = list(refs.values())[i:i+batch_size]
        for i, literature in enumerate(literatures):
            literature_prompts.append(literature_template.format(
                ref_id = str(i+1), ref_title = literature.base.title, ref_abstract = literature.base.abstract))
        literature_prompts.append("")
        user_all_prompt = ('---'.join(literature_prompts)).replace('{','{{').replace('}','}}')
        prompt_abstract = ChatPromptTemplate.from_messages([
            ("system", system_messsage), 
            ("user", user_all_prompt)])

        chain_abstract = prompt_abstract | model
        dump('preread_abstract_in', prompt_abstract.format())

        with get_openai_callback() as cb:
            res = chain_abstract.invoke(input={})
            print('total_tokens: ', cb.total_tokens)
            print('cost: ', cb.total_cost)

        output = res.content
        dump('preread_abstract_out', output)

        output = output.replace('\n\n','\n').split('---')

        if len(output)<len(literatures):
            raise ValueError('It seems that AI forget some items, please set a smaller batchsize and try again')
        for i in range(len(literatures)):
            literatures[i].suggestion = parse_AI_suggestion(output[i])
        
    reference.saveDetailReference(refs, ref_path)
    print(f'Finished preread_abstract, save to {ref_path}')

    return refs
