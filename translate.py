import sys
import time
from collections import defaultdict

import dill
from googletrans import Translator

from display_occurrences import load_dicts

SOURCE_LANG = 'sv'
TARGET_LANG = 'en'
MAX_LEN = 4970


def translate(source_folder, target_file):
    translator = Translator()

    complete_dictionary = load_dicts(source_folder)
    translated_dictionary = defaultdict(lambda: defaultdict(int))

    for pos in complete_dictionary:
        source_batch = []
        occurrences_batch = []
        source_bulk = ''
        occurrences = []
        translated_batch = []

        sorted_words = sorted(complete_dictionary[pos].items(), key=lambda x: x[1], reverse=True)
        for word, occurrence in sorted_words:
            source_bulk += word + '\n'
            occurrences.append(occurrence)

            if len(source_bulk) > MAX_LEN:
                source_batch.append(source_bulk)
                source_bulk = ''
                occurrences_batch.append(occurrences)
                occurrences = []
        source_batch.append(source_bulk)
        occurrences_batch.append(occurrences)

        for index, source_text in enumerate(source_batch):
            print(pos, index)
            delays = [0, 5, 10, 20, 30]
            for delay in delays:
                try:
                    if delay > 0:
                        print(f'Waiting {delay}s...')
                    time.sleep(delay)
                    translated_batch.append(translator.translate(source_text, src=SOURCE_LANG, dest=TARGET_LANG))
                    break
                except Exception:
                    continue

        for batch_index, translated_text in enumerate(translated_batch):
            separated_source_words = source_batch[batch_index].split('\n')
            separated_translated_words = translated_text.text.split('\n')
            for word_index, translated_word in enumerate(separated_translated_words):
                translated_dictionary[pos][(separated_source_words[word_index], translated_word.lower())] = \
                    occurrences_batch[batch_index][word_index]

    with open(target_file, 'wb') as f:
        dill.dump(translated_dictionary, f)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise ValueError('Following arguments mandatory: source_folder, target_file')
    translate(sys.argv[1], sys.argv[2])
