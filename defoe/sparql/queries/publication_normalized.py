"""
Counts total number of volumes, terms, words per year.
Use this query ONLY for normalizing the EB articles stored in the Knowledge Graph previously.
"""

from operator import add
from defoe import query_utils
from defoe.sparql.query_utils import blank_as_null
from pyspark.sql import SQLContext
from pyspark.sql.functions import col, when, count, sum
from pyspark.ml.feature import SQLTransformer
import yaml, os
from functools import partial, reduce


def do_query(df, config_file=None, logger=None, context=None):
    """
    Iterate through archives and count total number of documents,
    pages and words per year.

    For EB-ontology derived Knowledge Graphs, it returns result of form:

        {
          <YEAR>: [<NUM_VOLS>, <NUM_PAGES>, <NUM_TERMS>, <NUM_WORDS>],
          ...
        }
    Example:
      '1771':
      	- 3
      	- 2722
      	- 8923
      	- 1942064
      '1773':
     	- 3
     	- 2740
     	- 9187
     	- 1923682

    For NLS-ontology derived Knowledge Graphs, it returns result of form:
        {
          <YEAR>: [<NUM_VOLS>, <NUM_PAGES>,<NUM_WORDS>],
          ...
        }
    Example:
      '1671':
        - 1
        - 24
        - 4244
      '1681':
        - 1
        - 16
        - 4877

    :param archives: RDD of defoe.es.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: total number of documents, pages and words per year
    :rtype: list
    """

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    
    if "kg_type" in config:
        kg_type = config["kg_type"]
    else:
        kg_type = "total_eb"
    if kg_type == "total_eb" :
        fdf = df.withColumn("definition", blank_as_null("definition"))
        newdf=fdf.filter(fdf.definition.isNotNull()).select(fdf.year, fdf.volume, fdf.numPages, fdf.numWords)
    else:
        fdf = df.withColumn("text", blank_as_null("text"))
        newdf=fdf.filter(fdf.text.isNotNull()).select(fdf.year, fdf.vuri, fdf.volume, fdf.numPages, fdf.numWords)

    sqlTrans = SQLTransformer(
         statement="SELECT year, volume, vuri,  int(numPages), int(numWords) FROM __THIS__")
    newdf=sqlTrans.transform(newdf)
    ##### Number of Words

    num_words= newdf.groupBy("year").sum("numWords").withColumnRenamed("sum(numWords)", "tNumWords")
    #print("-------Num Words %s ----" % num_words.show())
    ### Num of Volumes ###
    if kg_type == "total_eb" :
        df_groups= newdf.groupBy("year", "volume", "numPages").count()
    else:
        df_groups= newdf.groupBy("year", "vuri", "volume", "numPages").count()

    if kg_type == "total_eb" :
        num_terms=df_groups.groupBy("year").sum("count").withColumnRenamed("sum(count)", "tNumTerms")
        #print("-------NumTerms %s ----" % num_terms.show())

    num_pages= df_groups.groupBy("year").sum("numPages").withColumnRenamed("sum(numPages)", "tNumPages")
    #print("-------NumPages %s ----" % num_pages.show())

    num_vol= df_groups.groupBy("year").count().withColumnRenamed("count", "tNumVol")
    #print("-------NumVolumes %s ----" % num_vol.show())

    
    
    vol_pages=num_vol.join(num_pages, on=["year"],how="inner")
    if kg_type == "total_eb" :
        vol_pages_terms=vol_pages.join(num_terms, on=["year"],how="inner")
        result=vol_pages_terms.join(num_words, on=["year"],how="inner")
    else:
        result=vol_pages.join(num_words, on=["year"],how="inner")
    result=result.toPandas()
    r={}
    for index, row in result.iterrows():
        year=row['year']
        r[year]=[]
        r[year].append(row["tNumVol"])
        r[year].append(row["tNumPages"])
        if kg_type == "total_eb":
            r[year].append(row["tNumTerms"])
        r[year].append(row["tNumWords"])
      
    return r
