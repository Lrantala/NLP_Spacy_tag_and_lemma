from __future__ import unicode_literals

import itertools
import spacy
import pandas as pd
pd.options.mode.chained_assignment = None
import logging
import csv
import regex as re
import os

def remove_line_changes(text):
    """Removes line change marks created by Spacy."""
    for line, word in enumerate(text):
        text[line] = str(word).replace("\n", " ")
    return text

def open_file(file):
    raw_table = pd.read_csv(file, sep=';', encoding='utf-8')
    return raw_table

def save_file(file, name):
    logging.debug("Entering writing pandas to file")
    try:
        filepath = "./save/"
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        file.to_csv(filepath + name + ".csv", encoding='utf-8', sep=";", quoting=csv.QUOTE_NONNUMERIC)
    except IOError as exception:
        print("Couldn't save the file. Encountered an error: %s" % exception)
    logging.debug("Finished writing: " + name)

def create_chunks(list, size):
    logging.debug("Creating a chunk")
    return (list[pos:pos + size] for pos in range(0, len(list), size))

def main():
    #Open file
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.debug("Entering main")

    #Load csv as pandas
    df = open_file("Comments0_210k_comments.csv")
    #df = open_file("Comments200_400k_comments.csv")
    #df = open_file("Comments400_rest_comments.csv")
    #df = open_file("10k-test_comments.csv")
    df.fillna('', inplace=True)


    #Spacy stuff
    logging.debug("Entering Spacy")
    nlp = spacy.load('en')
    #texts = df["text"]
    # df['tokenized'] = df['text'].apply(lambda x: nlp.tokenizer(x))
    # sentences = [sent.string.strip() for sent in doc.sents]
    # for row in sentences:
    #     print(row)




    # tokens = []
    # lemma = []
    # pos = []
# Iterating through the blocks of the big list
    count = 0
    for x in create_chunks(df, 10000):
        # tokens = []
        # lemma = []
        # pos = []
        # tag = []
        dep = []
        combined = []
        count += 1
        logging.debug("Starting iteration")
    # i = 0
        for doc in nlp.pipe(x['text'].astype('unicode').values):
            # for doc in nlp.pipe(df['text'].astype('unicode').values):
            #     i += 1
            #     if i % 10000 == 0:
            #         print(i)
            if doc.is_parsed:
                #
                # tokens.append([n.text for n in doc])
                # lemma.append([n.lemma_ for n in doc])
                # pos.append([n.pos_ for n in doc])
                # tag.append([n.tag_ for n in doc])
                # dep.append([n.dep_ for n in doc])

                # This was used originally. Gives only simple POS tags.
                # combined.append([(n.lemma_, n.pos_) for n in doc])
                combined.append([(n.lemma_, n.tag_, n.dep_) for n in doc])
            else:
                # We want to make sure that the lists of parsed results have the
                # same number of entries of the original Dataframe, so add some blanks in case the parse fails
                combined.append(None)
                # tokens.append(None)
                # lemma.append(None)
                # pos.append(None)
                # tag.append(None)
        #
        print("Setting tokens to df")
        x["lemma_tag_dep"] = combined
        # x['tokens'] = tokens
        # x['lemmas'] = lemma
        # x['pos'] = pos

        # df['tokens'] = tokens
        # df['lemmas'] = lemma
        # df['pos'] = pos
        # #
        # print(df[1:10])
        save_file(x, str(count))

    # save_file(df)
    logging.debug("All processed and saved. Resetting dataframe.")
    df = []


if __name__ == '__main__':
    main()
    logging.debug("Program ran successfully.")