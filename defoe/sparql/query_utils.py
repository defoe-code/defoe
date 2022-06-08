"""
Query-related utility functions.
"""
import re
from defoe import query_utils
from pyspark.sql.functions import col, when

def get_sentences_list_matches(text, keysentence):
    """
    Check which key-sentences from occurs within a string
    and return the list of matches.

    :param text: text
    :type text: str or unicode
    :type: list(str or uniocde)
    :return: Set of sentences
    :rtype: set(str or unicode)
    """
    match = []
    text_list= text.split()
    for sentence in keysentence:
        if len(sentence.split()) > 1:
            if sentence in text:
                count = text.count(sentence)
                for i in range(0, count):
                    match.append(sentence)
        else:
            pattern = re.compile(r'^%s$'%sentence)
            for word in text_list:
                if re.search(pattern, word):
                    match.append(sentence)
    return sorted(match)

def get_articles_list_matches(text, keysentence):
    
    """
    o	Article count: The query counts as a “hint” every time that finds an article with a particular term from our lexicon in the previously selected articles (by the target words or/and time period).  So, if a term is repeated several times in an article, it will be counted just as ONE. In this way, we are basically calculating the “frequency of articles” over time. 

    Check which key-sentences from occurs within a string
    and return the list of matches.

    :param text: text
    :type text: str or unicode
    :type: list(str or uniocde)
    :return: Set of sentences
    :rtype: set(str or unicode)
    """

    match = []
    text_list= text.split()
    for sentence in keysentence:
        if len(sentence.split()) > 1:
            if sentence in text:
                match.append(sentence)

        else:
            pattern = re.compile(r'^%s$'%sentence)
            for word in text_list:
                if re.search(pattern, word) and (sentence not in match):
                    match.append(sentence)
    return sorted(match)

def get_articles_text_matches(text, keysentence):
    
    """
     TERM count: The query counts as a “hint” every time that finds a hit with a particular term from our lexicon in the previously selected articles (by the target words or/and time period).  So, if a term is repeated several times in an article, it will be counted SEVERAL TIMES

    Check which key-sentences from occurs within a string
    and return the list of matches.

    :param text: text
    :type text: str or unicode
    :type: list(str or uniocde)
    :return: Set of sentences
    :rtype: set(str or unicode)
    """
    match_text = {}
    for sentence in keysentence:
        if len(sentence.split()) > 1:
            if sentence in text:
                if sentence not in match_text:
                    match_text[sentence]=text
        else:
            text_list= text.split()
            pattern = re.compile(r'^%s$'%sentence)
            for word in text_list:
                if re.search(pattern, word) and (sentence not in match_text):
                    match_text[sentence] = text
    return match_text

def blank_as_null(x):
    return when(col(x) != "", col(x)).otherwise(None)
