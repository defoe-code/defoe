"""
Gets concordance of window for keysentence and groups by date.
"""

from operator import add
from defoe import query_utils
from defoe.nls.query_utils import preprocess_clean_page, clean_page_as_string
from defoe.nls.query_utils import get_text_keyword_idx, get_concordance_string

import yaml, os

def do_query(archives, config_file=None, logger=None, context=None):
    """
    Gets concordance using a window of words, for keywords and groups by date.

    Data in ES have the following colums:

    "title",  "edition", "year", "place", "archive_filename", 
    "source_text_filename", "text_unit", "text_unit_id", 
    "num_text_unit", "type_archive", "model", "source_text_raw", 
    "source_text_clean", "source_text_norm", "source_text_lemmatize", "source_text_stem",
    "num_words"

    config_file must be the path to a configuration file with a list
    of the keywords to search for, one per line.

    Both keywords and words in documents are normalized, by removing
    all non-'a-z|A-Z' characters.

    Returns result of form:
          [(year, [(title, edition, archive_filename, filename, word,corcondance),
              (title, edition, archive_filename, filename, word, concordance ), ...]), ...]


    :param issues: RDD of defoe.alto.issue.Issue
    :type issues: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: information on documents in which keywords occur grouped
    by date
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

    window = 20
    preprocess_type = query_utils.extract_preprocess_word_type(config)
    preprocess_config = config["preprocess"]
    data_file = query_utils.extract_data_file(config,
                                              os.path.dirname(config_file))
    
    #newdf=fdf.filter(fdf.source_text_clean.isNotNull()).filter(fdf["model"]=="nls").select(fdf.year, fdf.title, fdf.edition, fdf.archive_filename, fdf.source_text_filename, fdf.source_text_clean)


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

    # [(year, document, title, edition, archive_filename), ...]
    documents = archives.flatMap(
        lambda archive: [(document.year, document, document.title, document.edition, document.archive.filename ) for document in list(archive)])
    # [(year, page_string)
    
    #(year, title, edition, archive_filename, page_code, clean_page_string)
    clean_pages = documents.flatMap(
        lambda year_document: [(year_document[0], year_document[2], year_document[3], year_document[4], page.code,
                                    clean_page_as_string(page, defoe_path, os_type)) 
                                       for page in year_document[1]])

    #(year, title, edition, archive_filename, page_code, preprocess_clean_page)
    pages = clean_pages.flatMap(
        lambda cl_page: [(cl_page[0], cl_page[1], cl_page[2], cl_page[3], cl_page[4],
                                    preprocess_clean_page(cl_page[5], preprocess_type))]) 
    #(year, title, edition, archive_filename, page_code, preprocess_clean_page)
    filter_pages = pages.filter(
        lambda year_page: any(
            keysentence in year_page[5] for keysentence in keysentences))

    # [(year, title, edition, archive_filename, filename, text, [(word, idx), (word, idx) ...]), ...]
    maching_idx = filter_pages.map(
        lambda year_page: (
            (year_page[0],
             year_page[1],
             year_page[2],
             year_page[3],
             year_page[4],
             year_page[5],
             get_text_keyword_idx(year_page[5],
                                     keysentences))
        )
    )

    # [(year, [(title, edition, archive_filename, filename, word, [concordance, ...]), ...])]
    concordance_words = maching_idx.flatMap(
        lambda year_idx: [
            (year_idx[0],
                {"title":year_idx[1], "edition": year_idx[2], "archive_filename": year_idx[3], "filename":year_idx[4], "term": word_idx[0],\
                 "snippet": get_concordance_string(year_idx[5], word_idx[0], word_idx[1], window)})\
                 for word_idx in year_idx[6]])

    result = concordance_words.groupByKey() \
        .map(lambda year_match:
             (year_match[0], list(year_match[1]))) \
        .collect()
    return result

