"""
Select the EB articles using a keysentences or keywords list and groups by date.
Use this query ONLY for searching in the EB articles stored in the Knowledge Graph previously.
"""

from operator import add
from defoe import query_utils
from defoe.sparql.query_utils import get_articles_list_matches, blank_as_null, get_articles_text_matches
from pyspark.sql import SQLContext
from pyspark.sql.functions import col, when
from defoe.nls.query_utils import preprocess_clean_page
import yaml, os
from functools import partial, reduce

def do_query(df, config_file=None, logger=None, context=None):
    """
    IMPORTANT: SAME AS "keysearch_by_year_term_count.py" in NLS!!

    Data in sparql have the following colums:
    
    config_file must be the path to a lexicon file with a list of the keywords 
    to search for, one per line.
    
    Also the config_file can indicate the preprocess treatment, along with the defoe
    path, and the type of operating system. 

      Returns result of form:
        {
          <YEAR>:
          [
            [ -<SENTENCE|WORD>, NUM_SENTENCES|NUM_WORDS 
             - <SENTENCE|WORD>, NUM_SENTENCES|NUM_WORDS 
             - <SENTENCE|WORD>, NUM_SENTENCES|NUM_WORDS 
            ], 
          <YEAR>:
          ...
        }
  
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
        config = yaml.safe_load(f)
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
    
    if "target_sentences" in config:
        target_sentences=config["target_sentences"]
    else:
        target_sentences = None

    if "target_filter" in config:
        target_filter=config["target_filter"]
    else:
        target_filter = "or"

    if "hit_count" in config:
        hit_count = config["hit_count"]

    else:
        hit_count = "term"

    if "kg_type" in config:
        kg_type = config["kg_type"]
    else:
        kg_type = "total_eb"

    ###### Supporting New NLS KG #######
    if kg_type == "total_eb" :
    
        fdf = df.withColumn("definition", blank_as_null("definition"))

        if start_year and end_year:
            newdf=fdf.filter(fdf.definition.isNotNull()).filter(fdf.year >= start_year).filter(fdf.year <= end_year).select(fdf.year, fdf.term, fdf.definition)
        elif start_year:
            newdf=fdf.filter(fdf.definition.isNotNull()).filter(fdf.year >= start_year).select(fdf.year, fdf.term, fdf.definition)
        elif end_year:
            newdf=fdf.filter(fdf.definition.isNotNull()).filter(fdf.year <= end_year).select(fdf.year, fdf.term, fdf.definition)
        else:
            newdf=fdf.filter(fdf.definition.isNotNull()).select(fdf.year, fdf.term, fdf.definition)

    else:
        fdf = df.withColumn("text", blank_as_null("text"))

        if start_year and end_year:
            newdf=fdf.filter(fdf.text.isNotNull()).filter(fdf.year >= start_year).filter(fdf.year <= end_year).select(fdf.year, fdf.text)
        elif start_year:
            newdf=fdf.filter(fdf.text.isNotNull()).filter(fdf.year >= start_year).select(fdf.year, fdf.text)
        elif end_year:
            newdf=fdf.filter(fdf.text.isNotNull()).filter(fdf.year <= end_year).select(fdf.year, fdf.text)
        else:
            newdf=fdf.filter(fdf.text.isNotNull()).select(fdf.year, fdf.text)

    articles=newdf.rdd.map(tuple)
    

    #(year-0, preprocess_article-1)
    if kg_type == "total_eb" :
        preprocess_articles = articles.flatMap(
            lambda t_articles: [(t_articles[0], preprocess_clean_page(t_articles[1]+ " " + t_articles[2], preprocess_type))]) 
    else:
        preprocess_articles = articles.flatMap(
            lambda t_articles: [(t_articles[0], preprocess_clean_page(t_articles[1], preprocess_type))]) 

    if data_file:
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



    if target_sentences:
        clean_target_sentences = []
        for target_s in list(target_sentences):
            t_split = target_s.split()
            sentence_word = [query_utils.preprocess_word(
                word, preprocess_type) for word in t_split]
            sentence_norm = ''
            for word in sentence_word:
                if sentence_norm == '':
                    sentence_norm = word
                else:
                    sentence_norm += " " + word
            clean_target_sentences.append(sentence_norm)
        if target_filter == "or":
            target_articles = preprocess_articles.filter(
                lambda year_page: any( target_s in year_page[1] for target_s in clean_target_sentences))
        else:
            target_articles = preprocess_articles
            target_articles = reduce(lambda r, target_s: r.filter(lambda year_page: target_s in year_page[1]), clean_target_sentences, target_articles)
        
    else:
        target_articles = preprocess_articles

    if data_file:
        filter_articles = target_articles.filter(
            lambda year_page: any( keysentence in year_page[1] for keysentence in keysentences))
    else:
        filter_articles = target_articles
        keysentences = clean_target_sentences


    #(year-0, list_sentences-1)

    if hit_count == "term" or hit_count == "page":
        matching_articles = filter_articles.map(
            lambda year_article: (year_article[0], 
                                     get_articles_list_matches(year_article[1], keysentences)))
    else:
        matching_articles = filter_articles.map(
            lambda year_article: (year_article[0], 
                                     get_articles_text_matches(year_article[1], keysentences)))
    
    #(year-0, sentence-1)
    matching_sentences = matching_articles.flatMap(
        lambda year_sentence: [((year_sentence[0], sentence),1) for sentence in year_sentence[1]])

    # [((year, keysentence), num_keysentences), ...]
    # =>
    # [(year, (keysentence, num_keysentences)), ...]
    # =>
    # [(year, [keysentence, num_keysentences]), ...]

    result = matching_sentences\
        .reduceByKey(add)\
        .map(lambda yearsentence_count:
             (yearsentence_count[0][0],
              (yearsentence_count[0][1], yearsentence_count[1]))) \
        .groupByKey() \
        .map(lambda year_sentencecount:
             (year_sentencecount[0], list(year_sentencecount[1]))) \
        .collect()
    return result
