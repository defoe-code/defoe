"""
Count concordance (also called details) occurrences of keywords or keysentences (by page) and group by year
"""

from operator import add

from defoe import query_utils
from defoe.nls.query_utils import preprocess_clean_page, clean_page_as_string
from defoe.nls.query_utils import get_sentences_list_matches

import yaml, os

def do_query(archives, config_file=None, logger=None, context=None):
    """
    Gets the concordance (also called details) occurrences of keywords or keysentences and groups by year.

    The config_file must indicate the path to a lexicon file with a list of the keywords 
    to search for, one per line.
    
    Also the config_file can indicate the preprocess treatment, along with the defoe
    path, and the type of operating system.

    Returns result of form:

        {
          <YEAR>:
          [
            - [title:
             place:
             publisher:
             snippet:
             term:
             document_id:
             filenanme]
            - []
            ...
          ],
          <YEAR>:
          ...
        }
        
       

    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: number of occurrences of keywords grouped by year
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
        lambda archive: [(document.year, document) for document in list(archive)])
    # [(year, page_string)
    
    
    clean_pages = documents.flatMap(
        lambda year_document: [(year_document[0], year_document[1], page,  
                                    clean_page_as_string(page, defoe_path, os_type)) 
                                       for page in year_document[1]])
    pages = clean_pages.flatMap(
        lambda cl_page: [(cl_page[0], cl_page[1], cl_page[2], 
                                    preprocess_clean_page(cl_page[3], preprocess_type))]) 
    # [(year, page_string)
    # [(year, page_string)
    filter_pages = pages.filter(
        lambda year_page: any(
            keysentence in year_page[1] for keysentence in keysentences))
    
    
    # [(year, [keysentence, keysentence]), ...]
    matching_pages = filter_pages.map(
        lambda year_page: (year_page[0], year_page[1], year_page[2], 
                              get_sentences_list_matches(
                                  year_page[3],
                                  keysentences)))
    
    matching_sentences = matching_pages.flatMap(
        lambda year_sentence: [(year_sentence[0], year_sentence[1], year_sentence[2], sentence)\
                                for sentence in year_sentence[3]])

    matching_data = matching_sentences.map(
        lambda page_data:
        (page_data[0],
         {"title": page_data[1].title,
          "place": page_data[1].place,
          "publisher": page_data[1].publisher,
          "page_number": page_data[2].code,
          "snippet": page_data[2].content,
          "term": page_data[3],
          "document_id": page_data[1].code,
          "filename": page_data[1].archive.filename}))

    
    result = matching_data \
        .groupByKey() \
        .map(lambda date_context:
             (date_context[0], list(date_context[1]))) \
        .collect()
    return result

     


