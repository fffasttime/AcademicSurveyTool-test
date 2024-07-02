from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.callbacks import get_openai_callback
from typing import Dict

import reference
from paper_data import MainSection, PaperData
from utils import dump

write_main_system_prompt = """
You are an academic literature survey writting helper. User want to write a content section of a survey. The paper title, section title and beginning of the section will be provided. You need to write a section according to some provided reference paper title, abstract, reference suggestions. Please try to align the quality of the output with the actual paper to minimize the need for user modifications. Remember that a good survey not only lists the key points of the references, but also summarizes and evaluates their ideas and makes meaningful criticisms and suggestions. You can also use your imagination to make extended discussions or research prospective. Expanding user provided beginnings is possible. Your output needs to meet the Latex format. Starting with \section{{section title}}. You can use \subsection{{}} divide content into 1~3 subsection to make the logic clearer and easier to read if needed, but should be as small as possible, so each subsection contains several similar literatures. Use \cite{{}} to cite literature key provided by the user. The user input begin by paper and current section information, followed by some literature data to be cited.
"""

section_user_prompt = """
Paper title: {title}
{addition_tldr}
Current section title to be write: {section_title}
Section beginning: {section_beginning}
---
{references}
"""

section_reference_user_prompt = """
reference key: {key}
literature title: {title}
abstract: {abstract}
brief: {relation}
cite suggestion: {suggestion}
"""

def write_main_section(section: MainSection, paper_data: PaperData, refs: reference.RefsType, LLM):
    literature_prompts = []
    for key in section.ref_entries:
        ref: reference.DetailReference = refs[key]
        literature_prompts.append(section_reference_user_prompt.format(
                key = key,
                title = ref.base.title, 
                abstract = ref.base.abstract,
                relation = ref.suggestion.relation,
                suggestion = ref.suggestion.suggestion,
            ))
    literature_all_prompt = '---'.join(literature_prompts)
    
    prompt_abstract = ChatPromptTemplate.from_messages([
        ("system", write_main_system_prompt), 
        ("user", section_user_prompt)])
    
    invoke_dict = {
        "title": paper_data.title,
        "addition_tldr": paper_data.addition_tldr,
        "section_title": section.title,
        "section_beginning": section.beginning,
        "references": literature_all_prompt 
    }
    
    dump('write_main_section_in', prompt_abstract.format(**invoke_dict))

    chain_abstract = prompt_abstract | LLM
    
    with get_openai_callback() as cb:
        res = chain_abstract.invoke(input=invoke_dict)
        print('total_tokens: ', cb.total_tokens)
        print('cost: ', cb.total_cost)
    
    section.final_content = res.content
    dump('write_main_section_out', res.content)
    

def write_main_sections(paper_data: PaperData, refs: reference.RefsType, LLM):
    assert len(paper_data.main_sections)
    for section in paper_data.main_sections:
        if section.final_content is not None and section.final_content!='':
            print(f'Skipping writting section {section.title}')
            continue
        else:
            input(f"Enter to write section {section.title}")

        write_main_section(section, paper_data, refs, LLM)
        
        paper_data.save("paperdata_main_writing.json")
