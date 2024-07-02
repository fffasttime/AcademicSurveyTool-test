from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.callbacks import get_openai_callback
from typing import Dict

import reference
import json
import re
import os

from paper_data import PaperData, MainSection
from utils import dump

write_frame_system_prompt = """
You are an academic literature review helper. User want to write a literature review titled "{title}"{addition_tldr}. You need to write an section outline of a literature review based on the literature titles and citation suggestions provided by the user. You need to classify and sort these literature reasonably to make the paper have a clear logical structure. Each literature provided by the user includes 4 fields: citation ID, title, a brief summary of the paper content related to the target and citation suggestions of the paper to this topic. Try to use all literature mentioned by users as much as possible. The number of sections divided should not exceed 6 because grained division can be in subsection.
The first section of the paper is the introduction, so you need to arrange the content of the following main sections. Your output needs to strictly follow JSON format section list with the following structure. Each section containing the following fields: title(the proposed section title), beginning(the beginning of the section review), reference(selected relevant reference IDs for this section). The following is the JSON format reference from another DL autonomous driving survey paper:
{example}
"""
write_frame_system_prompt_example="""[
{"title": "section 2: Overview of Deep Learning Technologies",
"beginning": "In this section, we describe the basis of deep learning technology used in autonomous vehicles and comments on the capabilities of each paragraph. We focus on Convoluus International Neural Networks (CNN), Recurrent Neural Networks (RNN), and Deep Reinforcement Learning (DRL), which are the most common deep learning methods applied to autonomous driving.",
"reference": [2,3,6,7,11]
},
{"title": "section 3: Deep Learning for Driving Scene Perception and Localization",
"beginning": "Beginning of section 3...",
"reference": [4,5,9,13,20]
}
]"""

read_user_prompt = """
ID: {id}
title: {title}
brief: {relation}
suggestion: {suggestion}
"""

def write_frame(paper_data: PaperData, refs: dict[str, reference.DetailReference], model):
    if len(paper_data.main_sections):
        print("paper_data.main_sections already exist, skipping write_frame")
        return
    else:
        input("Enter to write_frame")

    literature_prompts = []
    for i, literature in enumerate(refs.values()):
        if literature.suggestion.rating < 4:
            continue
        literature_prompts.append(read_user_prompt.format(
                id = str(i+1), 
                title = literature.base.title, 
                relation = literature.suggestion.relation,
                suggestion = literature.suggestion.suggestion
            ))

    user_all_prompt = ('---'.join(literature_prompts)).replace('{','{{').replace('}','}}')


    invoke_dict = {
        "example": write_frame_system_prompt_example,
        "title": paper_data.title,
        "addition_tldr": paper_data.addition_tldr,
        "user_reference_list": user_all_prompt,
    }
    prompt_frame = ChatPromptTemplate.from_messages([
        ("system", write_frame_system_prompt), 
        ("user", "{user_reference_list}")])
    chain = prompt_frame | model
    dump('writeframe_in', prompt_frame.format(**invoke_dict))

    with get_openai_callback() as cb:
        res = chain.invoke(invoke_dict)
        print('total_tokens: ', cb.total_tokens)
        print('cost: ', cb.total_cost)

    print(res.content)
    dump('writeframe_out', res.content)

    parse_frame_json(paper_data, refs, res.content)

def parse_frame_json(paper_data: PaperData, refs, content: str):
    literature_keys = []

    for key in refs:
        literature_keys.append(key)

    try:
        json_begin = content.index('[')
        json_end = content.rindex(']') + 1

        content = content[json_begin:json_end]

        res_list = json.loads(content)
        for section in res_list:
            keys = []
            for ID in section['reference']:
                keys.append(literature_keys[ID - 1])
            paper_data.main_sections.append(
                MainSection(
                    section['title'],
                    section['beginning'],
                    keys,
                    ''
                )
            )

    except Exception as e:
        print("LLM output json format is illegal, please consider fix it")
        raise e
