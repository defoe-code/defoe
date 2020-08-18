"""
Query-related utility functions.
"""

from defoe import query_utils
from defoe.query_utils import PreprocessWordType, longsfix_sentence, xml_geo_entities_snippet, georesolve_cmd,  coord_xml_snippet, geomap_cmd, geoparser_cmd, geoparser_coord_xml
from nltk.corpus import words
import re
import spacy
from spacy.tokens import Doc
from spacy.vocab import Vocab
NON_AZ_REGEXP = re.compile('[^a-z]')
from nltk.corpus import words



def get_pages_matches_no_prep(title, edition, archive, filename, text, keysentences):
    """
    Get pages within a document that include one or more keywords.
    For each page that includes a specific keyword, add a tuple of
    form:

        (<TITLE>, <EDITION>, <ARCHIVE>, <FILENAME>, <TEXT>, <KEYWORD>)

    If a keyword occurs more than once on a page, there will be only
    one tuple for the page for that keyword.
    If more than one keyword occurs on a page, there will be one tuple
    per keyword.

    :return: list of tuples
    """  
    matches = []
    for keysentence in keysentences:
        #sentence_match = get_sentences_list_matches(text, keysentence)
        sentence_match_idx = get_text_keyword_idx(text, keysentence)
        if sentence_match: 
            match = (title, edition, archive, filename, text, keysentence)
            matches.append(match) 
    return matches



def get_page_matches(document,
                     keywords,
                     preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Get pages within a document that include one or more keywords.
    For each page that includes a specific keyword, add a tuple of
    form:

        (<YEAR>, <DOCUMENT>, <PAGE>, <KEYWORD>)

    If a keyword occurs more than once on a page, there will be only
    one tuple for the page for that keyword.
    If more than one keyword occurs on a page, there will be one tuple
    per keyword.

    :param document: document
    :type document: defoe.nls.document.Document
    :param keywords: keywords
    :type keywords: list(str or unicode:
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: list of tuples
    :rtype: list(tuple)
    """
    matches = []
    for keyword in keywords:
        for page in document:
            match = None
            for word in page.words:
                preprocessed_word = query_utils.preprocess_word(
                    word, preprocess_type)
                if preprocessed_word == keyword:
                    match = (document.year, document, page, keyword)
                    break
            if match:
                matches.append(match)
                continue  # move to next page
    return matches


def get_document_keywords(document,
                          keywords,
                          preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Gets list of keywords occuring within an document.

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
    for page in document:
        for word in page.words:
            preprocessed_word = query_utils.preprocess_word(word,
                                                            preprocess_type)
            if preprocessed_word in keywords:
                matches.add(preprocessed_word)
    return sorted(list(matches))


def document_contains_word(document,
                           keyword,
                           preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Checks if a keyword occurs within an article.

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
    for page in document:
        for word in page.words:
            preprocessed_word = query_utils.preprocess_word(word,
                                                            preprocess_type)
            if keyword == preprocessed_word:
                return True
    return False


def calculate_words_within_dictionary(page, 
                   preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Calculates the % of page words within a dictionary and also returns the page quality (pc)
    Page words are normalized. 
    :param page: Page
    :type page: defoe.nls.page.Page
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :return: matches
    :rtype: list(str or unicode)
    """
    dictionary = words.words()
    counter= 0
    total_words= 0
    for word in page.words:
         preprocessed_word = query_utils.preprocess_word(word, preprocess_type)
         if preprocessed_word!="":
            total_words += 1
            if  preprocessed_word in dictionary:
               counter +=  1
    try:
       calculate_pc = str(counter*100/total_words)
    except:
       calculate_pc = "0" 
    return calculate_pc

def calculate_words_confidence_average(page):
    """
    Calculates the average of "words confidence (wc)"  within a page.
    Page words are normalized. 
    :param page: Page
    :type page: defoe.nls.page.Page
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :return: matches
    :rtype: list(str or unicode)
    """
    dictionary = words.words()
    counter= 0
    total_wc= 0
    for wc in page.wc:
               total_wc += float(wc)
    try:
       calculate_wc = str(total_wc/len(page.wc))
    except:
       calculate_wc = "0" 
    return calculate_wc

def get_page_as_string(page,
                          preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    Return a page as a single string.

    :param page: Page
    :type page: defoe.nls.Page
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: page words as a string
    :rtype: string or unicode
    """
    page_string = ''
    for word in page.words:
        preprocessed_word = query_utils.preprocess_word(word,
                                                         preprocess_type)
        if page_string == '':
            page_string = preprocessed_word
        else:
            page_string += (' ' + preprocessed_word)
    return page_string


def clean_page_as_string(page, defoe_path, os_type):
        
    """
    Clean a page as a single string,
    Handling hyphenated words: combine and split and also fixing the long-s

    :param page: Page
    :type page: defoe.nls.Page
    :return: clean page words as a string
    :rtype: string or unicode
    """
    page_string = ''
    for word in page.words:
        if page_string == '':
            page_string = word 
        else:
            page_string += (' ' + word)

    page_separeted = page_string.split('- ')
    page_combined = ''.join(page_separeted)
    
    if (len(page_combined) > 1) and ('f' in page_combined): 
       
       page_clean = longsfix_sentence(page_combined, defoe_path, os_type) 
    else:
        page_clean= page_combined

    page_final=page_clean.split()
    page_string_final = ''
    for word in page_final:
        if "." not in word:
            separated_str = re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', word)
        else:
            separated_str = word

        if page_string_final == '':
            page_string_final = separated_str
        else:
            page_string_final += (' ' + separated_str)
    return page_string_final

def preprocess_clean_page(clean_page,
                          preprocess_type=PreprocessWordType.LEMMATIZE):


    clean_list = clean_page.split(' ') 
    page_string = ''
    for word in clean_list:
        preprocessed_word = query_utils.preprocess_word(word,
                                                         preprocess_type)
        if page_string == '':
            page_string = preprocessed_word
        else:
            page_string += (' ' + preprocessed_word)
    return page_string

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
                match.append(sentence)

        else:
            pattern = re.compile(r'^%s$'%sentence)
            for word in text_list:
                if re.search(pattern, word) and (sentence not in match):
                    match.append(sentence)
    return sorted(match)


def get_sentences_list_matches_per_page(text,
                            keysentences):
    """
    Gets a list the total list of keywords within an
    article.

    :param text: text
    :type article: string
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :return: sorted list of keywords and their indices
    :rtype: list(tuple(str or unicode, int))
    """
    match = []
    text_list= text.split()
    for sentence in keysentences:
        if len(sentence.split()) > 1:
            if sentence in text:
                results=[matches.start() for matches in re.finditer(sentence, text)]
                for r in results:
                    match.append(sentence)
        else:
            pattern = re.compile(r'^%s$'%sentence)
            for word in text_list:
                if re.search(pattern, word):
                    match.append(sentence)
    return sorted(match)


def preprocess_clean_page_spacy(clean_page,
                          preprocess_type=PreprocessWordType.LEMMATIZE):


    clean_list = clean_page.split(' ')
    page_string = ''
    for word in clean_list:
        preprocessed_word = query_utils.preprocess_word(word,
                                                         preprocess_type)
        if page_string == '':
            page_string = preprocessed_word
        else:
            page_string += (' ' + preprocessed_word)
    return page_string


def preprocess_clean_page_spacy(clean_page):
    nlp = spacy.load('en')
    doc = nlp(clean_page)
    page_nlp_spacy=[]
    for i, word in enumerate(doc):
        word_normalized=re.sub(NON_AZ_REGEXP, '', word.text.lower())
        output="%d\t%s\t%s\t%s\t%s\t%s\t%s\t"%( i+1, word, word_normalized, word.lemma_, word.pos_, word.tag_, word.ent_type_)
        page_nlp_spacy.append(output)
    return page_nlp_spacy


def georesolve_page_2(text, lang_model, defoe_path, gazetteer, bounding_box):
    nlp = spacy.load(lang_model)
    doc = nlp(text)
    if doc.ents:
        flag,in_xml, snippet = xml_geo_entities_snippet(doc)
        if flag == 1:
            geo_xml=georesolve_cmd(in_xml, defoe_path, gazetteer, bounding_box)
            dResolved_loc= coord_xml_snippet(geo_xml, snippet)
            return dResolved_loc
        else:
           return {}
    else:
        return {}

def georesolve_page(doc):
    if doc.ents:
        flag,in_xml = xml_geo_entities(doc)
        if flag == 1:
            geo_xml=georesolve_cmd(in_xml)
            dResolved_loc= coord_xml(geo_xml)
            return dResolved_loc
        else:
           return {}
    else:
        return {}

def geoparser_page(text, defoe_path, os_type, gazetteer, bounding_box ):
    geo_xml=geoparser_cmd(text, defoe_path, os_type, gazetteer, bounding_box)
    dResolved_loc= geoparser_coord_xml(geo_xml)
    return dResolved_loc



def geomap_page(doc):
    geomap_html = ''
    if doc.ents:
        flag,in_xml = xml_geo_entities(doc)
        if flag == 1:
            geomap_html=geomap_cmd(in_xml)
    #return str(geomap_html)
    return geomap_html


def get_text_keyword_idx(text,
                            keywords):
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
    text_list= text.split()
    matches = set()
    for idx, word in enumerate(text_list):
        if  word in keywords:
            match = (word, idx)
            matches.add(match)
    return sorted(list(matches))


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


def get_concordance(text,
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

    concordance_words = []
    for word in text_list[start_idx:end_idx]:
        concordance_words.append(word)
    return concordance_words

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
