#!/usr/local/bin/python3
###################################
# CS B551 Fall 2019, Assignment #3
#
# Your names and user ids: dtolia kbhaler sporedi

import os
import re
import string
import sys
import math

# Parse for spam and not spam training data
def parse_directory(dir):
    irr_words_list = []
    # https://www.link-assistant.com/seo-stop-words.html
    irr_wrd = open("Irrelevant_words.txt", 'r')
    irr_words_list.append(line.strip() for line in irr_wrd)
    spam_words, spam_file_count, spam_word_count = parse_file(dir,"spam", irr_words_list)
    non_spam_words, non_spam_file_count, non_spam_word_count = parse_file(dir, "notspam", irr_words_list)
    return spam_words, spam_file_count, spam_word_count, non_spam_words, non_spam_file_count, non_spam_word_count

# Parse the training data for a class
def parse_file(dir, classify, irr_wrds_lst):
    train_words = dict()
    total_word_count = 0
    total_files_count = 0
    for fname in os.listdir(os.path.join(dir, classify)):
        try:
            # for encoding refered https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character
            file = open(os.path.join(dir, classify + "/" + fname), 'r', encoding='cp437')
            with file:
                # To remove html tags
                pt = re.sub(r'<*?>', "",file.read())
                # to remove newline escape characters
                line = re.split('\n| ',pt)
                for word in line:
                    # to remove trailing punctuation marks
                    lower_case_word = word.lower().strip(string.punctuation)
                    # check if the word is not in the list of words which are not relevant to emails Ex.'the', 'to', 'Jan', 'Mon'
                    if lower_case_word not in irr_wrds_lst:
                        # update word with its current count
                        if lower_case_word not in train_words:
                            train_words.setdefault(lower_case_word, 1)
                            total_word_count += 1
                        else:
                            word_count = train_words[lower_case_word]
                            word_count += 1
                            train_words.update({lower_case_word: word_count})
                            total_word_count += 1
            # count total number of files in a class
            total_files_count += 1
        except:
            print("Can't open file : ", fname)
    return train_words, total_files_count, total_word_count

# Creates a dictonary of words with its MAP values for both classes
def calc_map(s_words, s_count, ns_words, ns_count):
    map_table = dict()
    v_count = dict()
    v_count.update(s_words)
    v_count.update(ns_words)
    # Smoothening Factor
    m = 1
    v = len(v_count.keys())
    for word, count in s_words.items():
        if word in ns_words:
            ns_val = ns_words[word]
            # Delete words already added to map table from not spam class
            del ns_words[word]
        else:
            ns_val = 0
        map_table.setdefault(word, [(count+m)/(s_count+(m*v)), (ns_val+m)/(ns_count+(m*v))])
    s_val = 0
    # Remaining not spam words
    for word, count in ns_words.items():
        map_table.setdefault(word, [(s_val + m) / (s_count + (m * v)), (count + m) / (ns_count + (m * v))])
    return map_table

# Prediction for test data using the MAP values
def predict_with_map(map_table, dir, s_file_cnt, ns_file_cnt):
    prediction = dict()
    spam = dict()
    nspam = dict()
    s_prob = math.log(s_file_cnt)- math.log(s_file_cnt+ns_file_cnt)
    ns_prob = math.log(ns_file_cnt) - math.log(s_file_cnt+ns_file_cnt)
    for fname in os.listdir(dir):
        map_spam = 0.0
        map_ns = 0.0
        try:
            # for encoding refered https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character
            file = open(dir + "/" + fname, 'r', encoding='cp437')
            with file:
                # Remove html tags from the mail
                pt = re.sub(r'<*?>', "", file.read())
                # Remove escape character and space
                line = re.split('\n| ',pt)
                for word in line:
                    if word in map_table:
                        val = map_table[word]
                    else:
                        # As we round off at 8 decimal points
                        val = [0.00000001,0.00000001]
                    value_0 = round(float(val[0]), 8)
                    value_1 = round(float(val[1]), 8)
                    map_spam = map_spam + math.log(value_0)
                    map_ns = map_ns + math.log(value_1)
            # Prediction with MAP solution
            if (map_spam+s_prob) > (map_ns+ns_prob):
                spam.setdefault(fname, "spam")
            else:
                nspam.setdefault(fname, "notspam")
        except:
            print("Can't open file:", fname)
    prediction.update(spam)
    prediction.update(nspam)
    return prediction


# Main Function
if __name__ == "__main__":
    train_dir = sys.argv[1]
    test_dir = sys.argv[2]
    op_file = sys.argv[3]
    spam_words,spam_file_count, spam_word_count, non_spam_words, non_spam_file_count, non_spam_word_count = parse_directory(train_dir)
    map_table = calc_map(spam_words, spam_word_count, non_spam_words, non_spam_word_count)
    prediction = predict_with_map(map_table, test_dir,spam_file_count, non_spam_file_count)
    # Write the prediction in output file
    file = open(op_file, "w")
    for fname in prediction.keys():
        file.write("%s %s\n" % (fname, prediction[fname]))
    file.close()
