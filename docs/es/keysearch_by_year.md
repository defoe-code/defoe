# Read data from ES, and count number of occurrences of keywords or keysentences (by page) and group by year

* Read data previously stored in HDFS  
* Query module: `defoe.es.queries.keysearch_by_year`
* Configuration file:
  - preprocessing treatment to select (preprocess)
  - File with keywords or keysentece (data)
  - Examples:
     - preprocess: normalize
     - data: sc_cities.txt
* Result format:

```
<YEAR>:
- [<WORD|SENTENCE>, <NUM_WORDS|NUM_SENTENCES>]
- ...
<YEAR>:
...
```


**Note-1**: You will need to have the data previously stored in ES using `defoe.nls.queries.write_pages_df_es`.

**Important:** We recommend to read also the documentation for [writing and reading data from ES](../nls_demo_examples/nls_demo_individual_queries.md#writing-and-reading-data-tofrom-elasticsearch-es).
