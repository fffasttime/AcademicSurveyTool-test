import os

folder = 'preread_3/'

files = os.listdir(folder)

for file in files:
    with open(folder + file, encoding='utf-8') as f:
        print(file[:-4])
        print(f.read())
        print('------------------')
