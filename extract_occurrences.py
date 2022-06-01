import json
from collections import defaultdict
import sys
import dill

mapping = {
    'AB': 'ADV',
    'DT': 'DET',
    'HA': 'ADV',
    'HD': 'DET',
    'HP': 'PRON',
    'HS': 'PRON',
    'IE': 'PRT',
    'IN': 'X',
    'JJ': 'ADJ',
    'KN': 'CONJ',
    'NN': 'NOUN',
    'PC': 'ADJ',
    'PL': 'PRT',
    'PM': 'NOUN',
    'PN': 'PRON',
    'PP': 'ADP',
    'PS': 'PRON',
    'RG': 'NUM',
    'RO': 'NUM',
    'SN': 'CONJ',
    'VB': 'VERB',
    'UO': 'X',
    'MAD': '.',
    'MID': '.',
    'PAD': '.'
}


def parse_file(path, target):
    lemmas = defaultdict(lambda: defaultdict(int))
    index = 0
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('<w'):
                pos = ''
                lemma = ''

                atts = line.split(' ')
                for attr in atts:
                    if attr.startswith('lemma='):
                        lemma = attr.split('"')[1].split('|')
                        if len(lemma) > 2:
                            lemma = lemma[1]
                        else:
                            break
                    elif attr.startswith('pos='):
                        pos = mapping.get(attr.split('"')[1], 'X')
                        break

                if pos != '' and lemma != '':
                    lemmas[pos][lemma] += 1

                index += 1
                sys.stdout.write(f'\r{index}')

    with open(target, 'wb') as f:
        dill.dump(lemmas, f)


if __name__ == '__main__':
    parse_file(sys.argv[1], sys.argv[2])
