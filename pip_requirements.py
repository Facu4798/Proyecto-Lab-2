import os
fh = open('requirements.txt', 'r')
requirements = fh.readlines()
fh.close()

for r in requirements:
    r = r.strip()
    if r and not r.startswith('#'):
        os.system(f'pip install {r}')