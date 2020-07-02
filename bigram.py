#-*- coding: utf-8 -*-

from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
import nltk
import re


def bigram_rank(market_data):

    new_market_data = []
    temp_market_data = []
    word_sum_table, word_table = make_bigram_table(market_data)

    previous_shop_name = market_data[0][0]

    for product_element in market_data:

        current_shop_name = product_element[0]
        product_name = product_element[1]

        if current_shop_name != previous_shop_name:
            sort_market_data_by_bigram_probability = sorted(temp_market_data, key = lambda x: x[4], reverse = True)
            temp_market_data = sort_market_data_by_bigram_probability[:20]

            for element in temp_market_data:
                new_market_data.append(element)
                print element[0], element[1], element[2], element[3], element[4]

            temp_market_data = []
            previous_shop_name = current_shop_name

        parsed_product_name = new_word_parsing_rule(product_name)
        if parsed_product_name == "":
            continue

        parsed_product_name = parsed_product_name.strip()

        # Divide sentences based on the '.'
        sentence_in_text = []
        sentence = ""

        for word_index in range(len(parsed_product_name)):
            word = parsed_product_name[word_index]
            if word == "." and parsed_product_name[word_index - 1] == " ":
                sentence = sentence.strip()
                sentence_in_text.append(sentence)
                sentence = ""
                continue
            sentence += word

        if sentence != "":
            sentence = sentence.strip()
            sentence_in_text.append(sentence)

        total_bigram_probability = 1

        for sentence_element in sentence_in_text:

            parsed_text = sentence_element

            tokenized_text = word_tokenize(parsed_text)

            first_word = "_bos"
            second_word = parsed_text.split()[0].lower()

            bigram_probability = float(word_table[first_word][second_word] / float(word_sum_table[first_word]))

            for token_index in range(len(tokenized_text)-1):
                first_word = tokenized_text[token_index]
                second_word = tokenized_text[token_index+1]

                word_pair_probability = float(word_table[first_word][second_word] / float(word_sum_table[first_word]))
                bigram_probability *= word_pair_probability

            first_word = second_word
            second_word = "_eos"
            word_pair_probability = float(word_table[first_word][second_word] / float(word_sum_table[first_word]))
            bigram_probability *= word_pair_probability 

            total_bigram_probability *= bigram_probability

        temp_market_data.append([product_element[0], product_element[1], product_element[2], product_element[3], total_bigram_probability])

    sort_market_data_by_bigram_probability = sorted(temp_market_data, key = lambda x: x[4], reverse = True)
    temp_market_data = sort_market_data_by_bigram_probability[:20]

    for element in temp_market_data:
        new_market_data.append(element)
        print element[0], element[1], element[2], element[3], element[4]

    return new_market_data  

def make_bigram_table(market_data):

    word_table = defaultdict(dict)
    word_sum_table = dict()

    word_sum_table["_bos"] = 0

    for product_element in market_data:

        product_name = product_element[1]
        parsed_text = new_word_parsing_rule(product_name)

        if parsed_text == "":
            continue

        parsed_text = parsed_text.strip()

        # Divide sentences based on the '.'
        sentence_in_text = []
        sentence = ""

        for word_index in range(len(parsed_text)):
            word = parsed_text[word_index]
            if word == "." and parsed_text[word_index - 1] == " ":
                sentence = sentence.strip()
                sentence_in_text.append(sentence)
                sentence = ""
                continue
            sentence += word

        if sentence != "":
            sentence = sentence.strip()
            sentence_in_text.append(sentence)

        for sentence_element in sentence_in_text:

            parsed_text = sentence_element

            # add '!bos', loglevel as word pair
            # '!bos' means beginning of the string, '!eos' means end of the string
            first_word = "_bos"
            second_word = parsed_text.split()[0].lower()

            word_sum_table[first_word] += 1

            if second_word not in word_table[first_word].keys():
                word_table[first_word][second_word] = 0
            word_table[first_word][second_word] += 1

            temp_text = word_tokenize(parsed_text)
            # make word pairs and count them
            word_pair = BigramCollocationFinder.from_words(temp_text)

            # put word pairs to frequency table, and score at frequency sum table
            for pair, freq in word_pair.ngram_fd.items():
                first_word = pair[0]
                second_word = pair[1]
                if (first_word not in word_sum_table.keys()):
                    word_sum_table[first_word] = 0

                if (second_word not in word_table[first_word].keys()):
                    word_table[first_word][second_word] = 0

                word_table[first_word][second_word] += freq
                word_sum_table[first_word] += 1

            first_word = temp_text[-1]
            second_word = "_eos"
            if (first_word not in word_sum_table.keys()):
                word_sum_table[first_word] = 0
            if second_word not in word_table[first_word].keys():
                word_table[first_word][second_word] = 0

            word_sum_table[first_word] += 1
            word_table[first_word][second_word] += 1

    return word_sum_table, word_table 

def new_word_parsing_rule(log_text):

    # change all letter case to lower case
    temp_logtext = log_text.lower()
    # punctuation is special characters. (ex: ! , ? ~ ...)
    # add square brackets to make 'string.punctuatioin' to regular expression
    punctuation = """[!#$%&()*+,/:;<=>?@[\\]^`{|}~]"""

    # remove unnecessary words 
    # following 4 rules

    # 1. remove character in brackets or quotes

    # if brackets are not balanced, delete words after brackets.
    open_bracket = ["[", "{", "("]
    close_bracket = ["]", "}", ")"]

    # if 'character' is open bracket, add it to the 'open_brack_stack'
    # if 'character' is close bracket, check 'open_brack_stack'
    # check whether 'open_brack_stack' has vaule or top value of the stack is match bracket
    # if NOT, remove the words after first bracket in logtext
    open_brack_stack = []
    temp_logtext = list(temp_logtext)
    
    for char_index in range(len(temp_logtext)):

        character = temp_logtext[char_index]

        if character in open_bracket:
            open_brack_stack.append((character, char_index))
        elif character in close_bracket:
            close_brack_index = close_bracket.index(character)
            if ((len(open_brack_stack) > 0) and (open_bracket[close_brack_index] == open_brack_stack[-1][0])):
                for i in range(open_brack_stack[-1][1], char_index + 1):
                    temp_logtext[i] = " "
                open_brack_stack.pop()
            else:
                temp_logtext = temp_logtext[:char_index]
                break

    # multiple whitespaces to one whitespace
    temp_logtext = "".join(temp_logtext)
    temp_logtext = " ".join(temp_logtext.split())

    if len(open_brack_stack) > 0:
        bracket_match = re.search('[\(\{\[\]\}\)]', temp_logtext)
        first_brack_index = bracket_match.start()
        temp_logtext = temp_logtext[:first_brack_index]                    

    # 2. remove special character
    temp_logtext = re.sub(punctuation, " ", temp_logtext)
    temp_logtext = re.sub("\.\*", " ", temp_logtext)
    temp_logtext = re.sub("\'(.*)\'", " ", temp_logtext)
    temp_logtext = re.sub("\"(.*)\"", " ", temp_logtext)
    temp_logtext = re.sub(r'\\|\\\\'," ",temp_logtext)
    temp_logtext = re.sub("[\.]{2,}",".",temp_logtext)
    temp_logtext = re.sub("[-]{2,}","-",temp_logtext)
    temp_logtext = re.sub("[_]{2,}","_",temp_logtext)

	# 3. remove words less than 2 in length
    # except preposition or subordinating conjunction(IN), cordinating conjunction(CC), determiner(DT), 'to'(TO), and verb less two words(VB, VBD, VBG, VBN, VBP, VBZ)
    # 'pos' means 'part of speech'
    excluded_pos = ["IN", "CC", "DT", "TO", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

    # 4. remove words made up of numbers only or numbers and alphabet
    temp_logtext = re.sub("([\._-]*[a-zA-Z]*[\._-]*[0-9]+[\._-]*[a-zA-Z]*)+", " ", temp_logtext)

    # to check word's pos, logtext must be tokenized
    # 'temp_logtex_token' means list of tokenized logtext
    temp_logtext_token = nltk.word_tokenize(temp_logtext)
    for token_index in range(len(temp_logtext_token)):
        if len(temp_logtext_token[token_index]) <= 2:
            if re.match("[\.]",temp_logtext_token[token_index]):
                continue
            
            pos = nltk.pos_tag([temp_logtext_token[token_index]])
            if pos[0][1] not in excluded_pos:
                temp_logtext_token[token_index] = ""

    # join token list to 'temp_logtext'
    temp_logtext = " ".join(temp_logtext_token)

    return temp_logtext