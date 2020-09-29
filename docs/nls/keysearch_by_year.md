# Count number of occurrences of keywords or keysentences and group by year

* Both keywords/keysentences and words in documents are normalized, by removing all non-'a-z|A-Z' characters.
* Query module: `defoe.nls.queries.keysentence_by_year`
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
- [<WORD>, <NUM_WORDS>]
- ...
<YEAR>:
...
```

