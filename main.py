import json
import os
import re
import time
from typing import List

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.callbacks import get_openai_callback

from utils import dump, read_dump
import reference
from preread_abstract import preread_abstract
from paper_data import PaperData, MainSection
from write_frame import write_frame, parse_frame_json
from main_sections import write_main_sections

API_KEY = "sk-********************************"
PROXY = "socks5://localhost:port"
os.environ['http_proxy'] = PROXY
os.environ['https_proxy'] = PROXY

model_gpt35 = ChatOpenAI(model='gpt-3.5-turbo-0125', openai_api_key=API_KEY, openai_proxy=PROXY, temperature=0.2)
model_gpt4 = ChatOpenAI(model='gpt-4-0125-preview', openai_api_key=API_KEY, openai_proxy=PROXY, temperature=0.2)

write_introduction_system_prompt = """
You are an academic literature survey writing helper. User want to write first introduction section of a literature survey. The main content section will be provided by user. Your output needs to meet the Latex format, starting with \section{{Introduction}}. Your output should not contain any extra format prompt like ```latex.
"""
write_introduction_user_prompt = """
I'm writing a literature review titled "{title}"{addition_tldr}.
Help me write introduction section. Main part of my paper:
{content}
"""

write_abstract_system_prompt = """
You are an academic literature review writing helper.
"""
write_abstract_user_prompt = """
I'm writing a literature review titled "{title}"{addition_tldr}.
Help me write content of abstract. You only need to give me result without any extra prompt. This is introduction of my paper:
{content}
"""

def write_introduction(paper_data: PaperData, LLM):
    if paper_data.introduction_section != '':
        print('Skipping write_introduction')
        return
    else:
        input('Enter to write_introduction')
    
    assert paper_data.main_sections[0].final_content != ''

    paper_prompt = '\n'.join([section.final_content for section in paper_data.main_sections])
    
    prompt_abstract = ChatPromptTemplate.from_messages([
        ("system", write_introduction_system_prompt), 
        ("user", write_introduction_user_prompt)])
    
    invoke_dict = {
        "title": paper_data.title,
        "addition_tldr": paper_data.addition_tldr,
        "content": paper_prompt,
    }
    
    dump('write_introduction_in', prompt_abstract.format(**invoke_dict))

    chain_abstract = prompt_abstract | LLM
    
    with get_openai_callback() as cb:
        res = chain_abstract.invoke(input=invoke_dict)
        print('total_tokens: ', cb.total_tokens)
        print('cost: ', cb.total_cost)
    
    paper_data.introduction_section = res.content
    dump('write_introduction_out', res.content)

def write_abstract(paper_data: PaperData, LLM):
    if paper_data.abstract != '':
        print('Skipping write_abstract')
        return
    else:
        input('Enter to write_abstract')
    
    assert paper_data.introduction_section != ''

    prompt_abstract = ChatPromptTemplate.from_messages([
        ("system", write_abstract_system_prompt), 
        ("user", write_abstract_user_prompt)])
    
    invoke_dict = {
        "title": paper_data.title,
        "addition_tldr": paper_data.addition_tldr,
        "content": paper_data.introduction_section,
    }
    
    dump('write_abstract_in', prompt_abstract.format(**invoke_dict))

    chain_abstract = prompt_abstract | LLM
    
    with get_openai_callback() as cb:
        res = chain_abstract.invoke(input=invoke_dict)
        print('total_tokens: ', cb.total_tokens)
        print('cost: ', cb.total_cost)
    
    paper_data.abstract = res.content
    dump('write_abstract_out', res.content)

def get_intro():
    # refs = reference.readbib()
    # reference.matchPDFs(refs, 'refpdfAI')

    refs = reference.loadPDFs('refpdftest')
    reference.saveDetailReference(refs, 'refpdftest.json')

def write_final_content(paper_data: PaperData, filename):
    with open(filename, 'w') as f:
        print("Title:", paper_data.title, file=f)
        print(file=f)
        print(paper_data.abstract, file=f)
        print(file=f)
        print(paper_data.introduction_section, file=f)
        print('\n'.join([section.final_content for section in paper_data.main_sections]), file=f)

if __name__ == '__main__':
    paper_data_file = 'paperdata_main_writing.json'
    if os.path.exists(paper_data_file):
        print("Use existed paper data file", paper_data_file)
        paper_data = PaperData.load(paper_data_file)
    else:
        paper_data = PaperData(
            title = "A survey of hardware error fault tolerance for deep learning",
            addition_tldr = "(Hardware fault tolerance includes hardware related fault tolerance evaluation and fault tolerance design, with the aim of avoiding deep learning computational errors caused by hardware circuit errors.)",
            main_sections = [],
        )
        # paper_data = PaperData(
        #     title = "A survey of RTL simulation acceleration",
        #     addition_tldr = "",
        #     main_sections = [],
        # )

    # refs = preread_abstract(paper_data, 'reliAI.bib', model_gpt4)
    # refs = preread_abstract(paper_data, 'rtl.bib', model_gpt4)
    refs = preread_abstract(paper_data, 'relix.bib', model_gpt4)

    if True:
        write_frame(paper_data, refs, model_gpt4)
    else: # 
        if len(paper_data.main_sections):
            input("paper_data.main_sections already exist, Enter to skip parse_frame_json")
        else:
            parse_frame_json(paper_data, refs, read_dump('writeframe_out_0105124247'))
            paper_data.save("paperdata_mid.json")

    paper_data.save("paperdata_mid_gpt4.json")

    write_main_sections(paper_data, refs, model_gpt4)
    
    write_introduction(paper_data, model_gpt4)
    write_abstract(paper_data, model_gpt4)
    paper_data.save("paperdata_final4.json")

    write_final_content(paper_data, 'relix_gpt4.txt')

    # get_intro()

    # write_frame_md()
