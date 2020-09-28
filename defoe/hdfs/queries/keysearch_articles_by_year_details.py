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

    Data in HDFS have the following colums:
    
    "title",  "edition", "year", "place", "archive_filename",  "source_text_filename", "text_unit", 
    "text_unit_id", "num_text_unit", "type_archive", "model", "type_page", "header", "term", "definition",
    "num_articles", "num_page_words", "num_article_words", 

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
        config = yaml.load(f)
    preprocess_type = query_utils.extract_preprocess_word_type(config)
    data_file = query_utils.extract_data_file(config,
                                              os.path.dirname(config_file))
    # Filter out the pages that are null, which model is nls, and select only 2 columns: year and the page as string (either raw or preprocessed).
    fdf = df.withColumn("definition", blank_as_null("definition"))
    #(year, title, edition, archive_filename, page_filename, page_number, type of page, header, term, article_text)
    newdf=fdf.filter(fdf.definition.isNotNull()).filter(fdf["model"]=="nlsArticles").select(fdf.year, fdf.title, fdf.edition, fdf.archive_filename, fdf.source_text_filename, fdf.text_unit_id, fdf.type_page, fdf.header, fdf.term, fdf.definition)
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

    #(year, title, edition, archive_filename, page_filename, page_number, type of page, header, article, preprocess_article, clean_article)
   
    preprocess_articles = articles.flatMap(
        lambda t_articles: [(t_articles[0], t_articles[1], t_articles[2], t_articles[3], t_articles[4], t_articles[5],
                                    t_articles[6], t_articles[7], t_articles[8],
                                        preprocess_clean_page(t_articles[9], preprocess_type), t_articles[9])]) 

     
    filter_articles = preprocess_articles.filter(
        lambda year_page: any( keysentence in year_page[9] for keysentence in keysentences))



    #(year, title, edition, archive_filename, page_filename, page_number, type of page, header, term, article_text, list_sentences)
    matching_articles = filter_articles.map(
        lambda year_article: (year_article[0], year_article[1], year_article[2], year_article[3], 
                                year_article[4], year_article[5], year_article[6], year_article[7],
                                    year_article[8], year_article[10], get_articles_list_matches(year_article[9], keysentences)))
    
    #(year, title, edition, archive_filename, page_filename, page_number, type of page, header, term, article_text, sentence)
    matching_sentences = matching_articles.flatMap(
        lambda year_sentence: [(year_sentence[0], year_sentence[1], year_sentence[2], year_sentence[3],
                                year_sentence[4], year_sentence[5], year_sentence[6], year_sentence[7],
                                year_sentence[8], year_sentence[9], sentence)\
                                for sentence in year_sentence[10]])

    matching_data = matching_sentences.map(
        lambda sentence_data:
        (sentence_data[0],
        {"title": sentence_data[1],
         "edition": sentence_data[2],
         "archive_filename": sentence_data[3],
         "filename": sentence_data[4],
         "page number": sentence_data[5],
          "type_page": sentence_data[6],
          "header": sentence_data[7],
          "term": sentence_data[10],
          "article": sentence_data[8],
          "article-definition": sentence_data[9]}))

    # [(date, {"title": title, ...}), ...]
    # =>
    
    result = matching_data \
        .groupByKey() \
        .map(lambda date_context:
             (date_context[0], list(date_context[1]))) \
        .collect()
    return result

     
