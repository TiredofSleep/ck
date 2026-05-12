import re
with open('sprint18_dark_sector.tex', 'r', encoding='utf-8') as f:
    content = f.read()

cites = re.findall(r'\\cite\{([^}]+)\}', content)
unique_cites = set()
for c in cites:
    for x in c.split(','):
        unique_cites.add(x.strip())
print('Unique citations used:')
for c in sorted(unique_cites):
    print(f'  {c}')
print()

bibitems = re.findall(r'\\bibitem\{([^}]+)\}', content)
print('Defined bibitems:')
for b in sorted(bibitems):
    print(f'  {b}')

undefined = unique_cites - set(bibitems)
unused = set(bibitems) - unique_cites
print(f'\nCitations not defined: {sorted(undefined)}')
print(f'Bibitems unused: {sorted(unused)}')
