"""
Counts total number of documents, pages and words per year.
It uses HDFS pre-stored data. 

This can be useful if wanting to see how the average number of
documents, pages and words change over time, for example.
"""


def do_query(archives, config_file=None, logger=None, context=None):
    """
    Iterate through archives and count total number of documents,
    pages and words per year.

    Returns result of form:

        {
          <YEAR>: [<NUM_DOCUMENTS>, <NUM_PAGES>, <NUM_WORDS>],
          ...
        }

    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: total number of documents, pages and words per year
    :rtype: list
    """
    newdf=fdf.filter(fdf.definition.isNotNull()).select(fdf.year, fdf.archive_filename, fdf.num_pages)
    articles=newdf.rdd.map(tuple)
    archive_df= newdf.groupby("archive_filename", "year","num_pagest").count()
    #>>> archive_df.show()
    # +--------------------+----+---------------+-----+
    # |    archive_filename|year|num_text_units |count|
    # +--------------------+----+---------------+-----+
    # |/mnt/lustre/at003...|1842|      810      |  785|
    # |/mnt/lustre/at003...|1778|      886      |  829|
    # |/mnt/lustre/at003...|1810|      446      |  422|
    # |/mnt/lustre/at003...|1823|      878      |  833|
    # +--------------------+----+---------+-----------+

    # I need to take the number of words per page!
    #todo return result
