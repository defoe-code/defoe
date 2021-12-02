"""
Select the EB articles using a keysentences or keywords list and groups by date.
Use this query ONLY for searching in the EB articles stored in HDFS previously 
using nlsArticles/write_articles_pages_df_hdfs.py query. 
"""

from operator import add
from defoe import query_utils
from defoe.hdfs.query_utils import get_articles_list_matches, blank_as_null
from pyspark.sql import SQLContext
from pyspark.sql.functions import col, when
from defoe.nls.query_utils import preprocess_clean_page
import yaml, os

def do_query(df, config_file=None, logger=None, context=None):
    """
    Gets concordance using a window of words, for keywords and groups by date.

    Data in sparql have the following colums:
    
    "archive_filename", definition, edition, header|page|term| title| uri|volume|year"

    config_file must be the path to a lexicon file with a list of the keywords 
    to search for, one per line.
    
    Also the config_file can indicate the preprocess treatment, along with the defoe
    path, and the type of operating system. 

      Returns result of form:
        {
          <YEAR>:
          [
            [- title: 
             - edition:
             - archive_filename:
             - page number:
             - header:
             - term:
             - article:
             - article-definition: ], 
             [], 
            ...
         
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
    data_file = query_utils.extract_data_file(config,
                                              os.path.dirname(config_file))
    # Filter out the pages that are null, which model is nls, and select only 2 columns: year and the page as string (either raw or preprocessed).
    fdf = df.withColumn("definition", blank_as_null("definition"))
    #(year-0, definition-1)
    newdf=fdf.filter(fdf.definition.isNotNull()).select(fdf.year, fdf.definition)
    articles=newdf.rdd.map(tuple)
    

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

  
    #(year-0, preprocess_article-1)

    preprocess_articles = articles.flatMap(
        lambda t_articles: [(t_articles[0], preprocess_clean_page(t_articles[1], preprocess_type))]) 

     
    filter_articles = preprocess_articles.filter(
        lambda year_page: any( keysentence in year_page[1] for keysentence in keysentences))



    #(year-0, list_sentences-1)
    matching_articles = filter_articles.map(
        lambda year_article: (year_article[0], 
                                 get_articles_list_matches(year_article[1], keysentences)))
    
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
