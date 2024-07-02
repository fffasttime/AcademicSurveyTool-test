
import time

def dump(file, s):
    now = time.strftime(r'_%m%d%H%M%S')
    with open('log/' + file + now + '.txt', 'w', encoding='utf-8') as f:
        f.write(s)

def read_dump(file):
    with open('log/' + file + '.txt', 'r') as f:
        content = f.read()
    return content
