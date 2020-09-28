"""
The query counts as a “hit” every time that finds a page with a particular term from a lexicon
and it groups the results by books.
"""

from operator import add

from defoe import query_utils
from defoe.nls.query_utils import preprocess_clean_page, clean_page_as_string
from defoe.nls.query_utils import get_sentences_list_matches

import yaml, os

def do_query(archives, config_file=None, logger=None, context=None):
    """
    The query counts as a “hit” every time that finds a page with a particular 
    term from a lexicon and it groups the results by years.
    
    config_file must be the path to a lexicon file with a list of the keywords 
    to search for, one per line.
    
    Also the config_file can indicate the preprocess treatment, along with the defoe
    path, and the type of operating system.

    Example:
        '''Twas on the morn of sweet May Day':
            - - neu
                 - 1
            - - blaw
                 - 4
    That means that neu appears in one page of the book 'Twas on the morn of sweet May Day'. 
    And blaw appears in 4 pages of the same book.


    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: number of occurrences of keywords grouped bytitle
    :rtype: dict
    """
    with open(config_file, "r") as f:
        config = yaml.load(f)
    if "os_type" in config:
        if config["os_type"] == "linux":
            os_type = "sys-i386-64"
        else:
            os_type= "sys-i386-snow-leopard"
    else:
            os_type = "sys-i386-64"
    if "defoe_path" in config :
        defoe_path= config["defoe_path"]
    else:
        defoe_path = "./"

    preprocess_type = query_utils.extract_preprocess_word_type(config)
    data_file = query_utils.extract_data_file(config, os.path.dirname(config_file))
    keysentences = []
    with open(data_file, 'r') as f:
        for keysentence in list(f):
            k_split = keysentence.split()
            sentence_word = [query_utils.preprocess_word(
                word, preprocess_type) for word in k_split]
            sentence_norm = ''
            for word in sentence_word:
                if sentence_norm == '':
                    sentence_norm = word
                else:
                    sentence_norm += " " + word
            keysentences.append(sentence_norm)
    # [(year, document), ...]
    documents = archives.flatMap(
        lambda archive: [(document.title, document) for document in list(archive)])
    # [(year, page_string)
    
    
    clean_pages = documents.flatMap(
        lambda title_document: [(title_document[0],  
                                    clean_page_as_string(page, defoe_path, os_type)) 
                                       for page in title_document[1]])
    pages = clean_pages.flatMap(
        lambda cl_page: [(cl_page[0], 
                                    preprocess_clean_page(cl_page[1], preprocess_type))]) 
    # [(year, page_string)
    # [(year, page_string)
    filter_pages = pages.filter(
        lambda title_page: any(
            keysentence in title_page[1] for keysentence in keysentences))
    
    
    # [(year, [keysentence, keysentence]), ...]
    matching_pages = filter_pages.map(
        lambda title_page: (title_page[0],
                              get_sentences_list_matches(
                                 title_page[1],
                                  keysentences)))
    

    # [[(year, keysentence), 1) ((year, keysentence), 1) ] ...]
    matching_sentences = matching_pages.flatMap(
        lambda title_sentence: [((title_sentence[0], sentence), 1)
                               for sentence in title_sentence[1]])


    # [((year, keysentence), num_keysentences), ...]
    # =>
    # [(year, (keysentence, num_keysentences)), ...]
    # =>
    # [(year, [keysentence, num_keysentences]), ...]
    result = matching_sentences\
        .reduceByKey(add)\
        .map(lambda titlesentence_count:
             (titlesentence_count[0][0],
              (titlesentence_count[0][1], titlesentence_count[1]))) \
        .groupByKey() \
        .map(lambda title_sentencecount:
             (title_sentencecount[0], list(title_sentencecount[1]))) \
        .collect()
    return result
