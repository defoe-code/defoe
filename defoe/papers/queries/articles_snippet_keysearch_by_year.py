"""
Gets the snippet of each term (from a list of keywords or keysentences) along with the metadata.
We recommend to use this query when we want to select a window of words (snippet lenght) around each term, instead of selecting
all the words of the page in which the term was found

This query replace the following ones:
  - keyword_concordance_by_date.py 
  - target_concordance_collocation_by_date.py

"""

from operator import add

from defoe import query_utils
from defoe.papers.query_utils import preprocess_clean_article, clean_article_as_string
from defoe.papers.query_utils import get_text_keysentence_idx, get_concordance_string

import yaml, os

def do_query(issues, config_file=None, logger=None, context=None):
    """
    Select the articles text along with metadata by using a list of 
    keywords or keysentences and filter those by date. Results are grouped by year.

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
    
    Finally, to select the dates that we want to use in this query, we have to indicate them
    in the configuration file as follows:
    
      start_year: YEAR_START (including that year)
      end_year: YEAR_FINISH (including that year)

    Returns result of form:
        {
          <YEAR>:
          [
            [- article_id: 
             - authors:
             - filename:
             - issue_id:
             - page_ids:
             - text:
             - term
             - title ]
            ...
          ],
          <YEAR>:
          ...
        }

    :param issues: RDD of defoe.papers.issue.Issue
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
    if "data" in config:
        data_file = query_utils.extract_data_file(config,
                                              os.path.dirname(config_file))
    else:
        data_file = None

    if "start_year" in config:
        start_year = int(config["start_year"])
    else:
        start_year = None

    if "start_year" in config:
        end_year = int(config["end_year"])
    else:
        end_year = None
    
    if "num_target" in config:
        num_target=config["num_target"]
    else:
        num_target= None

    if "target_filter" in config:
        target_filter=config["target_filter"]
    else:
        target_filter = "or"

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
    
    if num_target:    
        target_sentences = keysentences[0:num_target]
    else
        target_sentences= None

    keysentences = keysentences[lexicon_start:]
    if start_year and end_year:
        clean_articles = issues.flatMap(
            lambda issue: [(issue.date.year, issue, article, clean_article_as_string(
                article, defoe_path, os_type), issue.filename, article.quality) for article in issue.articles if int(issue.date.year)>= start_year and int(issue.date.year)<= end_year])

    elif start_year:
        clean_articles = issues.flatMap(
            lambda issue: [(issue.date.year, clean_article_as_string(
                article, defoe_path, os_type),  issue.filename, article.quality) for article in issue.articles if int(issue.date.year)>= start_year])
    elif end_year:
        clean_articles = issues.flatMap(
            lambda issue: [(issue.date.year, clean_article_as_string(
                article, defoe_path, os_type),  issue.filename, article.quality) for article in issue.articles if int(issue.date.year)<= end_year])
    else:
        clean_articles = issues.flatMap(
            lambda issue: [(issue.date.year, clean_article_as_string(
                article, defoe_path, os_type),  issue.filename, article.quality) for article in issue.articles])

    
    # [(year, preprocess_article_string), ...]
    t_articles = clean_articles.flatMap(
        lambda cl_article: [(cl_article[0],  
                                    preprocess_clean_article(cl_article[1], preprocess_type), cl_article[2], cl_article[3])]) 
    if target_sentences:
        if target_filter == "or":
            target_articles = t_articles.filter(
                lambda year_article: any(
                target_s in year_article[1] for target_s in target_sentences))

        else:
            target_articles = t_articles
            target_articles = reduce(lambda r, target_s: r.filter(lambda year_page: target_s in year_article[1]), target_sentences, target_articles)
    else:
            target_articles = t_articles


    # [(year, clean_article_string, issue.filename, article.quality)
    filter_articles = target_articles.filter(
         lambda year_article: any(
            keysentence in year_article[1] for keysentence in keysentences))

    matching_idx = filter_articles.map(
        lambda year_article_file_ocr: (
            (year_article_file_ocr[0],
             year_article_file_ocr[1],
             year_article_file_ocr[2],
             get_text_keysentence_idx(year_article_file_orc[1],
                                     keysentences))
             year_article_file_ocr[3])
        )
    )

    # [(year, [(filename, word, [concordance, ...], ocr), ...])]
    concordance_words = matching_idx.flatMap(
        lambda year_article_file_matches_ocr: [
            (year_article_file_matches_ocr[0],
             (year_article_file_matches_ocr[2],
              word_idx[0],
              get_concordance_string(year_article_file_matches_ocr[1], 
                                     word_idx[0], 
                                     word_idx[1], 
                                     window)
              year_article_file_matches_ocr[4]))
            for word_idx in year_article_file_matches_ocr[3]])

    # [(year, [(filename, word, corcondance, ocr),
    #          (filename, word, concordance, ocr), ...]), ...]


    result = concordance_words.groupByKey() \
        .map(lambda year_match:
             (year_match[0], list(year_match[1]))) \
        .collect()
    return result
