write_frame_system_prompt = """
You are an academic paper literature review helper. User want to write a literature review titled "{title}"{addition_tldr}. You need to write an outline of a literature review based on the reference paper titles and citation suggestions provided by the user. You need to classify and sort these literature reasonably to make the paper have a clear logical structure. Each literature provided by the user includes a citation ID, title, a brief summary of content, citation suggestions, relevance rating (integer in 6-9) of the paper to this topic.
The first section of the paper is the introduction, so you need to arrange the content of the following main sections. Your output needs to follow a strict JSON format section list with the following structure, each section containing the following fields: title(the proposed section title), beginning(the beginning of the section review), reference(selected relevant reference IDs for this section). The following is the format reference for the output json from one DL autonomous driving survey paper:
{example}
"""
write_frame_system_prompt_example="""[
{"title": "section 2: Overview of Deep Learning Technologies",
"beginning": "In this section, we describe the basis of deep learning technology used in autonomous vehicles and comments on the capabilities of each paragraph. We focus on Convoluus International Neural Networks (CNN), Recurrent Neural Networks (RNN), and Deep Reinforcement Learning (DRL), which are the most common deep learning methods applied to autonomous driving.",
"reference": [2,3,6,7,11]
},
{"title": "section 3: Deep Learning for Driving Scene Perception and Localization",
"beginning": "Beginning of section 3...",
"reference": [4,5,9,13,20],
}
]
"""

def write_frame():
    files = os.listdir('preread_abs_3')
    segs = []
    for id, file in enumerate(files):
        with open('preread_abs_3/'+file, encoding="utf-8") as f:
            seggestion = f.read()
        seggestion = 'id: %d\n'%(id+1) + seggestion
        segs.append(seggestion)

    user_input = '\n---\n'.join(segs)
    
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = len(encoding.encode(user_input))
    print(f"Referece seggestions has {len(segs)} papers, total {tokens} tokens")
    dump('write_frame_in.txt', user_input)

    invoke_dict = {
        "example": write_frame_system_prompt_example,
        "title": title,
        "addition_tldr": addition_tldr,
        "user_reference_list": user_input,
    }
    prompt_frame = ChatPromptTemplate.from_messages([
        ("system", write_frame_system_prompt), 
        ("user", "{user_reference_list}")])
    chain_frame = prompt_frame | model

    res = chain_frame.invoke(invoke_dict)
    print(res.content)
    dump('write_frame_out.txt', res.content)

def write_frame_md():
    with open('write_frame_out_4.txt') as f:
        content = json.load(f)
    
    refs = reference.readbib()
    files = os.listdir('preread_abs_3')

    for section in content:
        print('##', section['title'])
        print(section['beginning'])
        
        for id in section['reference']:
            ref_abbr = files[id - 1][:-4]
            for paper in refs:
                if ref_abbr == paper.ref_abbr:
                    title = paper.title
                    break
            print('- ', ref_abbr, '-', title)
        print()