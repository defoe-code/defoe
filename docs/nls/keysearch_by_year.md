# Count number of pages in which appear keywords or keysentences and group by year

* Both keywords/keysentences and words in documents are cleaned (long-S and hyphen fixes) and preprocessed according to the configuration file
* Query module: `defoe.nls.queries.keysearch_by_year`
* Configuration file:
  - defoe path (defoe_path)
  - operating system (os) 
  - preprocessing treatment (preprocess)
  - File with keywords or keysentece (data)
  - Examples:
     - preprocess: normalize
     - data: sc_cities.txt
     - defoe_path: /lustre/home/sc048/rosaf4/defoe/
     - os_type: linux
* Result format:

```
<YEAR>:
- [<WORD | SENTENCES>, <NUM_WORDS | NUM_SENTENCES>]
- ...
<YEAR>:
...
```
Note: This query is the same as:  `defoe.nls.queries.keysearch_by_year_page_count`


