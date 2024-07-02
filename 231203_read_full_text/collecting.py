import os
import parse
import tiktoken
from pathlib import Path

def read_papers():
    dir = Path('refpdf')
    files = os.listdir(dir)

    for file in files:
        text = ""
        if file.endswith('.pdf'):
            text = parse.parsepdf(dir / file)
        
        if not text:
            continue
        
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokens = encoding.encode(text)
        print(f"Read paper {file}, got {len(tokens)} tokens")

        with open(f"txt/{file}.txt", "w", encoding="utf-8") as reader_logger:
            reader_logger.write(text)


if __name__=="__main__":
    read_papers()
