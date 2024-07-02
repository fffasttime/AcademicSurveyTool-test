
prompt = ChatPromptTemplate.from_messages([
    ("system", read_system_prompt), 
    ("user", read_user_prompt)])

chain = prompt | model

def preread_file(file):
    with open(f"txt/{file}.txt", "r", encoding="utf-8") as f:
       text = f.read()
       
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = len(encoding.encode(text))
    print(f"Read paper {file}, got {tokens} tokens")

    if tokens>12000: return

    invoke_dict = {
        "title": title,
        "addition_tldr": addition_tldr,
        "paper_title": file,
        "paper_text": text
    }

    res = chain.invoke(invoke_dict)
    print(file)
    print(res.content)

    with open('preread/'+file+'.txt', "w", encoding="utf-8") as f:
        f.write(res.content)

def preread():
    files = os.listdir('txt')
    for file in files:
        preread_file(file[:-4])
