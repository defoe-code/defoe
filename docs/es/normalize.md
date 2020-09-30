# Read data from ES, and perform the normalize query

Count total number of documents, pages and words per year. This can be useful if wanting to see how the average number of documents, pages and words change over time.
It uses ES data.

* Query module: `defoe.es.queries.normalize`
* Configuration file: None
* Result format:

```
<YEAR>: [<NUM_DOCUMENTS>, <NUM_PAGES>, <NUM_WORDS>]
...
```

**Note-1**: You will need to have the data previously stored in ES using `defoe.nls.queries.write_pages_df_es`.
