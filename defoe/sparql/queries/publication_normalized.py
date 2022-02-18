"""
Counts total number of terms, words per year.
Use this query ONLY for normalizing the EB articles stored in the Knowledge Graph previously.
"""

from operator import add
from defoe import query_utils
from defoe.sparql.query_utils import get_articles_list_matches, blank_as_null, get_articles_text_matches
from pyspark.sql import SQLContext
from pyspark.sql.functions import col, when
import yaml, os
from functools import partial, reduce

def do_query(df, config_file=None, logger=None, context=None):
    """
    Iterate through archives and count total number of documents,
    pages and words per year.

    Returns result of form:

        {
          <YEAR>: [<NUM_DOCUMENTS>, <NUM_WORDS>],
          ...
        }

    :param archives: RDD of defoe.es.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: total number of documents, pages and words per year
    :rtype: list
    """
    fdf = df.withColumn("definition", blank_as_null("definition"))
    newdf=fdf.filter(fdf.definition.isNotNull()).select(fdf.year, fdf.numWords)
    articles=newdf.rdd.map(tuple)
    # [(year, (1, num_words)), ...]
    #print("-------- %s ------" %articles.collect())
    counts = articles.map(lambda document:
                           (document[0],
                            (1, int(document[1]))))
    ## [(year, (num_documents, num_words)), ...]
    # =>
    ## [(year, [num_documents, num_words]), ...]

    result = counts \
        .reduceByKey(lambda x, y:
                     tuple(i + j for i, j in zip(x, y))) \
        .map(lambda year_data: (year_data[0], list(year_data[1]))) \
        .collect()
    return result
