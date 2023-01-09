"""
Query-related utility functions.
"""

from nltk.corpus import stopwords

from defoe import query_utils
from defoe.query_utils import PreprocessWordType, longsfix_sentence
from defoe.query_utils import PreprocessWordType
import re


def get_article_matches(issue,
                        keysentences, defoe_path, os_type,
                        preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    Get articles within an issue that include one or more keywords.
    For each article that includes a specific keyword, add a tuple of
    form:

        (<DATE>, <ISSUE>, <ARTICLE>, <KEYWORD>)

    If a keyword occurs more than once in an article, there will be
    only one tuple for the article for that keyword.

    If more than one keyword occurs in an article, there will be one
    tuple per keyword.

    :param issue: issue
    :type issue: defoe.alto.issue.Issue
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: list of tuples
    :rtype: list(tuple)
    """
    matches = []
    for keysentence in keysentences:
        for article in issue:
            sentence_match = None
            clean_article=clean_article_as_string(article, defoe_path, os_type)
            preprocess_article=preprocess_clean_article(clean_article, preprocess_type)
            sentence_match = get_sentences_list_matches(preprocess_article, keysentence)
            if sentence_match:
                match = (issue.date.date(), issue, article, keysentence, clean_article)
                matches.append(match)
    return matches


def get_article_keywords(article,
                         keywords,
                         preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    Get list of keywords occuring within an article.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: sorted list of keywords that occur within article
    :rtype: list(str or unicode)
    """
    matches = set()
    for word in article.words:
        preprocessed_word = query_utils.preprocess_word(word,
                                                        preprocess_type)
        if preprocessed_word in keywords:
            matches.add(preprocessed_word)
    return sorted(list(matches))


def article_contains_word(article,
                          keyword,
                          preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    Check if a keyword occurs within an article.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param keywords: keyword
    :type keywords: str or unicode
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: True if the article contains the word, false otherwise
    :rtype: bool
    """
    for word in article.words:
        preprocessed_word = query_utils.preprocess_word(word,
                                                        preprocess_type)
        if keyword == preprocessed_word:
            return True
    return False


def article_stop_words_removal(article,
                               preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    Remove the stop words of an article.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: article words without stop words
    :rtype: list(str or unicode)
    """
    stop_words = set(stopwords.words('english'))
    article_words = []
    for word in article.words:
        preprocessed_word = query_utils.preprocess_word(word, preprocess_type)
        if preprocessed_word not in stop_words:
            article_words.append(preprocessed_word)
    return article_words


def get_article_as_string(article,
                          preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    Return an article as a single string.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: article words as a string
    :rtype: string or unicode
    """
    article_string = ''
    for word in article.words:
        preprocessed_word = query_utils.preprocess_word(word, preprocess_type)
        if article_string == '':
            article_string = preprocessed_word
        else:
            article_string += (' ' + preprocessed_word)
    return article_string


def get_sentences_list_matches_2(text, keysentence):
    """
    Check which key-sentences from occurs within a string
    and return the list of matches.

    :param text: text
    :type text: str or unicode
    :param keysentence: sentences
    :type: list(str or uniocde)
    :return: Set of sentences
    :rtype: set(str or unicode)
    """
    match = set()
    for sentence in keysentence:
        if sentence in text:
            match.add(sentence)
    return sorted(list(match))


def get_article_keyword_idx(article,
                            keywords,
                            preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    Gets a list of keywords (and their position indices) within an
    article.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: sorted list of keywords and their indices
    :rtype: list(tuple(str or unicode, int))
    """
    matches = set()
    for idx, word in enumerate(article.words):
        preprocessed_word = query_utils.preprocess_word(word, preprocess_type)
        if preprocessed_word in keywords:
            match = (preprocessed_word, idx)
            matches.add(match)
    return sorted(list(matches))


def get_concordance(article,
                    keyword,
                    idx,
                    window,
                    preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    For a given keyword (and its position in an article), return
    the concordance of words (before and after) using a window.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param keyword: keyword
    :type keyword: str or unicode
    :param idx: keyword index (position) in list of article's words
    :type idx: int
    :window: number of words to the right and left
    :type: int
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: concordance
    :rtype: list(str or unicode)
    """
    article_size = len(article.words)

    if idx >= window:
        start_idx = idx - window
    else:
        start_idx = 0

    if idx + window >= article_size:
        end_idx = article_size
    else:
        end_idx = idx + window + 1

    concordance_words = []
    for word in article.words[start_idx:end_idx]:
        concordance_words.append(
            query_utils.preprocess_word(word, preprocess_type))
    return concordance_words



def clean_article_as_string(article, defoe_path, os_type):
        
    """
    Clean a article as a single string,
    Handling hyphenated words: combine and split and also fixing the long-s

    :param article: Article
    :type article: defoe.papers.article.Article
    :return: clean article words as a string
    :rtype: string or unicode
    """
    article_string = ''
    for word in article.words:
        if article_string == '':
            article_string = word
        else:
            article_string += (' ' + word)

    article_separete = article_string.split('- ')
    article_combined = ''.join(article_separete)
  
    if (len(article_combined) > 1) and ('f' in article_combined): 
       article_clean = longsfix_sentence(article_combined, defoe_path, os_type) 
       return article_clean
    else:
        return article_combined

def preprocess_clean_article(clean_article,
                          preprocess_type=PreprocessWordType.LEMMATIZE):


    clean_list = clean_article.split(' ') 
    article_string = ''
    for word in clean_list:
        preprocessed_word = query_utils.preprocess_word(word,
                                                         preprocess_type)
        if article_string == '':
            article_string = preprocessed_word
        else:
            article_string += (' ' + preprocessed_word)
    return article_string


def get_sentences_list_matches(text, keysentence):
    """
    Check which key-sentences from occurs within a string
    and return the list of matches.
    
    o	Term count: The query counts as a “hint” every time that finds a term from our lexicon in the previously selected articles (by the target words or/and time period).  So, if a term is repeated 10 times in an article, it will be counted as 10. In this way, we are basically calculating the “frequency of terms” over time.

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
    o	Article count: The query counts as a “hint” every time that finds an article with a particular term from our lexicon in the previously selected articles (by the target words or/and time period).  So, if a term is repeated several times in an article, it will be counted just as ONE. In this way, we are basically calculating the “frequency of articles” over time. 

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


def get_text_keysentence_idx(text,
                            keysentences):
    """
    Gets a list of keywords (and their position indices) within an
    article.

    :param text: text
    :type article: string
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :return: sorted list of keywords and their indices
    :rtype: list(tuple(str or unicode, int))
    """
    matches = []
    text_list= text.split()
    for sentence in keysentences:
        if len(sentence.split()) > 1:
            if sentence in text:
                results=[match.start() for match in re.finditer(sentence, text)]
                for r in results:
                    idx=len(text[0:r].split())
                    match=(sentence, idx)
                    matches.append(match)
        else:
            pattern = re.compile(r'^%s$'%sentence)
            for idx, word in enumerate(text_list):
                if re.search(pattern, word):
                    match=(word, idx)
                    matches.append(match)
    return sorted(matches)

def get_concordance_string(text,
                    keyword,
                    idx,
                    window):
    """
    For a given keyword (and its position in an article), return
    the concordance of words (before and after) using a window.

    :param text: text
    :type text: string
    :param keyword: keyword
    :type keyword: str or unicode
    :param idx: keyword index (position) in list of article's words
    :type idx: int
    :window: number of words to the right and left
    :type: int
    :return: concordance
    :rtype: list(str or unicode)
    """
    text_list= text.split()
    text_size = len(text_list)

    if idx >= window:
        start_idx = idx - window
    else:
        start_idx = 0

    if idx + window >= text_size:
        end_idx = text_size
    else:
        end_idx = idx + window + 1

    concordance_words = ''
    flag_first = 1
    for word in text_list[start_idx:end_idx]:
        if flag_first == 1:
            concordance_words += word
            flag_first = 0
        else:
            concordance_words += ' ' + word
    return concordance_words
