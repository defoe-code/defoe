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
    """
    fdf = df.withColumn("definition", blank_as_null("definition"))
    newdf=fdf.filter(fdf.definition.isNotNull()).select(fdf.year, fdf.title, fdf.edition, fdf.archive_filename, fdf.page, fdf.header, fdf.term, fdf.definition)
    articles=newdf.rdd.map(tuple)
    print(articles.collect())
    result={}
    return result

     
