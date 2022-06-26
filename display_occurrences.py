import os
import sys
from collections import defaultdict
import dill
from pprint import pprint


def load_dicts(folder):
    complete_dictionary = defaultdict(lambda: defaultdict(int))

    for file in os.listdir(folder):
        with open(folder + '/' + file, 'rb') as f:
            lemmas = dill.load(f)
            for pos in lemmas:
                for lemma in lemmas[pos]:
                    complete_dictionary[pos][lemma] += lemmas[pos][lemma]
    return complete_dictionary


def display_occurrences(folder, min_occurrence=1000, max_output=10, pos_list=None):
    complete_dictionary = load_dicts(folder)

    for pos in complete_dictionary:
        if len(pos_list) == 0 or pos in pos_list:
            print(pos, len(list(filter(lambda x: x > min_occurrence, complete_dictionary[pos].values()))))
            pprint(sorted(complete_dictionary[pos].items(), key=lambda x: x[1], reverse=True)[:max_output])


if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise ValueError('Following arguments mandatory: dir, min_occurrence, max_output, pos_list')
    display_occurrences(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:])
