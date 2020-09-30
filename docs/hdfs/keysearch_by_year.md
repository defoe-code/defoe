# Read data from HDFS, and count number of occurrences of keywords or keysentences (by page) and group by year

* Read data previously stored in HDFS  
* Query module: `defoe.hdfs.queries.keysentence_by_year`
* Configuration file:
  - preprocessing treatment to select (preprocess)
  - File with keywords or keysentece (data)
  - Examples:
     - preprocess: normalize
     - data: sc_cities.txt
* Result format:

```
<YEAR>:
- [<WORD | SENTENCE>, <NUM_WORDS|NUM_SENTENCES>]
- ...
<YEAR>:
...
```

**Note-1**: You will need to have the data previously stored in HDFS using `defoe.nls.queries.write_pages_df_hdfs`.

**Important:** We recommend to read also the documentation for [writing and reading data to/from HDFS](../nls_demo_examples/nls_demo_individual_queries.md#writing-and-reading-data-fromto-hdfs).
