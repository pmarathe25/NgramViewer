######################################################################################
# Pranav Marathe
# September 24, 2017
# This code parses books and creates dicitonaries of n-grams.
######################################################################################

import os
import re
import sys
import pickle
from collections import deque, defaultdict

def append_book_ngrams(book, ngrams, max_degree):
    """
    Appends all n-grams length 1 to n from a book to an existing list of dictionaries of n-grams.
    """
    print "Processing %r..." % book
    word_buffer = deque([""] * max_degree)
    with open(book) as f:
        for line in f:
            # Replace all non-word characters with spaces.
            for word in re.sub("[^a-zA-Z0-9' -]|( - )|(--)", ' ', line).split():
                # Generate all posisble n-grams using a deque
                word_buffer.append(word)
                word_buffer.popleft()
                # Now loop over the word buffer and create appropriate n-grams
                ngram = ""
                for index, word in enumerate(word_buffer):
                    ngram += " " + word
                    ngram = ngram.strip()
                    # Add to dictionary and also increment the total counts.
                    ngrams[index][0][ngram] += 1
                    ngrams[index][1] += 1

def process_year(year_dir, max_degree):
    """
    Creates a list of the form:

    [1-grams: [{word: count}, total], 2-grams: [{word: count}, total], ..., n-grams: [{word: count}, total] ]
    """
    ngrams = []
    for x in range(max_degree):
        ngrams.append([defaultdict(int), 0])
    # Now loop over all the books this year and create a dictionary file for n-grams.
    for book in [os.path.join(year_dir, s) for s in os.listdir(year_dir)]:
        append_book_ngrams(book, ngrams, max_degree)

    print ngrams[4][0]["of The Return of Tarzan"]

    return ngrams

def process_data(data_dir, processed_dir, max_degree):
    """
    Loops over every year and creates a pkl file.
    """
    # Loop over every year in the data set.
    for year_dir in os.listdir(data_dir):
        if os.path.isdir(os.path.join(data_dir, year_dir)):
            # Write the processed year to a file.
            with open(os.path.join(processed_dir, year_dir) + ".pkl", 'wb') as f:
                print year_dir
                pickle.dump(process_year(os.path.join(data_dir, year_dir), max_degree), f, pickle.HIGHEST_PROTOCOL)

def main():
    """
    Usage: python data_parser [DATA_DIR] [OUTPUT_DIR] [MAX_N]
    """
    data_dir = "data/" if len(sys.argv) < 2 else sys.argv[1]
    processed_dir = "processed/" if len(sys.argv) < 3 else sys.argv[2]
    max_degree = 5 if len(sys.argv) < 4 else sys.argv[3]
    # Process!
    process_data(data_dir, processed_dir, max_degree)

if __name__ == '__main__':
    main()
