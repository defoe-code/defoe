# Get concordance (also called details) occurrences of keywords or keysentences (by page) and group by year - Returns Full PAGE for each match

* Query module: `defoe.es.queries.keysentence_concordance_by_year`
* Configuration file:
  - preprocessing treatment (preprocess)
  - File with keywords or keysentece (data)
  - Examples:
     - preprocess: normalize
     - data: sc_cities.txt
* Result format:

```
<YEAR>:
- { title: <TITLE>,
    edition: <EDITION>,
    archive_name: <ARCHIVE>,
    filename: <FILENAME>,
    text: <PAGE CONTENT>,
    keysentence: <TERM>}
- ...
<YEAR>:
...
```

**Caution:** as this query returns each page's content, for every match, there is a risk that the query will fail due to lack of memory. This query should only be run with interesting words that are not expected to occur often. Otherwise, use `defoe.es.queries.window_concordance_by_date` query instead, since this one just retrieve a number of words (window) before and after each match.

**Important:** We recommend to read also the documentation for [writing and reading data/from ES](../nls_demo_examples/nls_demo_individual_queries.md#writing-and-reading-data-tofrom-elasticsearch-es).
