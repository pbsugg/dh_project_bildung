# program to run in python 3.5

import zipfile
from zipfile import ZipFile
import codecs
import nltk
# from nltk.corpus import stopwords
import string
import csv

# assuming for the moment that my target file is a series of zipped directories, organized by page, as documented here
# https://www.hathitrust.org/documents/HTRC-UnCamp2012-themed-htrc-api-overview-1.pdf

# "sample_volumes"are random snippets (with references to Bildung sprinkled throughout) from Humboldt's "Briefe an eine Freundin"
# http://onlinebooks.library.upenn.edu/webbin/gutbook/lookup?num=21801

target_file = zipfile.ZipFile('sample_volumes.zip', mode='r')
iterable_file_list = target_file.infolist()

# not doing stopwords for now
# stop = stopwords.words('german')

# occurrences is the array where I will store the results
occurrences = []

for text_file in iterable_file_list:
    name = text_file.filename
    # escaping directories, only want the page numbers themselves
    if name.endswith('.txt'):
        result = codecs.open(name, 'r', 'utf-8')
        content = result.read()
        tokenized = nltk.word_tokenize(content)
        # deciding not to remove stopwords for now, could change
        # for token in tokenized:
        #     if token in stop:
        #         tokenized.remove(token)

        # downcase the result
        cleaned_up_file = [token.lower() for token in tokenized]
        # removing punctuation words for now
        for word in cleaned_up_file:
            if word in string.punctuation:
                cleaned_up_file.remove(word)
        file_index_length = len(cleaned_up_file) - 1
        for center_index, word in enumerate(cleaned_up_file):
            # also searching for variants of bildung
            if "bildung" in word:
                # main logic to calculate the context on either side, want to make sure I don't go out of range
                if (center_index - 15 < 0):
                    start_index = 0
                else:
                    start_index = center_index - 15
                if (center_index + 15 > file_index_length):
                    end_index = file_index_length
                else:
                    end_index = center_index + 15
                # context_slice is the finished array context slice for each occurrence
                context_slice = cleaned_up_file[start_index:end_index]
                occurrences.append(context_slice)

# write result to a csv
# todo: may need to adjust write/row format but you get the idea.
# todo: no year data right now, because I don't know where I'll get it
# See "results.csv" for how this comes out

with open('result.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(occurrences)
