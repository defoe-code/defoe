"""
Select the articles text by keywords or keysentences and groups by year.
This query is the recommended to use when there are target words. 
"""

from operator import add

from defoe import query_utils
from defoe.papers.query_utils import preprocess_clean_article, clean_article_as_string
from defoe.papers.query_utils import get_sentences_list_matches, get_articles_list_matches

import yaml, os

def do_query(issues, config_file=None, logger=None, context=None):
    """
    Counts number of occurrences of keywords or keysentences and groups by year.

    
    config_file must be the path to a lexicon file with a list of the keywords 
    to search for, one per line.
    
    Also the config_file can indicate the preprocess treatment, along with the defoe
    path, and the type of operating system. We can also configure how many target words 
    we want to use, and in which position the lexicon words starts. 
    
    For indicating the number of target words to use from the lexicon file, we can indicate it 
    in the configuration file as, num_target: 1. That means, that we have only one word/sentence
    as the target word (the first one). 
    
    If we want to include the target words in the lexicon, we should indicate in 
    the configuration file as, lexicon_start: 0.
    
    If we do not want to include the target words (lets image that we have just one target word) 
    in the lexicon, we should indicate in the configuration file as, lexicon_start: 1.
    

    Returns result of form:

        {
          <YEAR>:
          [
            [<SENTENCE|WORD>, <NUM_SENTENCES|WORDS>],
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
    data_file = query_utils.extract_data_file(config,
                                              os.path.dirname(config_file))
    num_target=int(config["num_target"])
    lexicon_start= int(config["lexicon_start"])
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
    # [(year, article_string), ...]
    
    target_sentences = keysentences[0:num_target]
    keysentences = keysentences[lexicon_start:]
    clean_articles = issues.flatMap(
        lambda issue: [(issue.date.year, issue, article, clean_article_as_string(
            article, defoe_path, os_type)) for article in issue.articles])


    # [(year, preprocess_article_string), ...]
    t_articles = clean_articles.flatMap(
        lambda cl_article: [(cl_article[0], cl_article[1], cl_article[2],  
                                    preprocess_clean_article(cl_article[3], preprocess_type))]) 

    # [(year, clean_article_string)
    target_articles = t_articles.filter(
        lambda year_article: any(
            target_s in year_article[3] for target_s in target_sentences))

    # [(year, clean_article_string)
    filter_articles = target_articles.filter(
        lambda year_article: any(
            keysentence in year_article[3] for keysentence in keysentences))
    
    # [(year, [keysentence, keysentence]), ...]
    # Note: get_articles_list_matches ---> articles count
    # Note: get_sentences_list_matches ---> word_count 
     
    matching_articles = filter_articles.map(
        lambda year_article: (year_article[0], year_article[1], year_article[2], get_articles_list_matches(year_article[3], keysentences)))
    
    matching_sentences = matching_articles.flatMap(
        lambda year_sentence: [(year_sentence[0], year_sentence[1], year_sentence[2], sentence)\
                                for sentence in year_sentence[3]])

    matching_data = matching_sentences.map(
        lambda sentence_data:
        (sentence_data[0],
        {"title": sentence_data[2].title_string,
         "article_id:": sentence_data[2].article_id,
         "authors:": sentence_data[2].authors_string,
         "page_ids": list(sentence_data[2].page_ids),
          "term": sentence_data[3],
          "original text": sentence_data[2].words_string,
          "issue_id": sentence_data[1].newspaper_id,
          "filename": sentence_data[1].filename}))

    # [(date, {"title": title, ...}), ...]
    # =>
    
    result = matching_data \
        .groupByKey() \
        .map(lambda date_context:
             (date_context[0], list(date_context[1]))) \
        .collect()
    return result

     
