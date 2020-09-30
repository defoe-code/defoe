# Get concordance (also called details) occurrences of keywords or keysentences (by page) and group by year - Returns Full Page for each match

* Both keywords/keysentences and words in documents are cleaned (long-S and hyphen fixes) and preprocessed according to the configuration file
* Query module: `defoe.nls.queries.keysentence_by_year_details`
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
- { title: <TITLE>,
    place: <PLACE>,
    publisher: <PUBLISHER>,
    page_number: <PAGE_NUMBER>,
    snippet: <PAGE CONTENT>,
    term: <WORD>,
    document_id: <DOCUMENT_ID>,
    filename: <FILENAME>}
- ...
<YEAR>:
...
```


**Caution:** as this query returns each page's content, for every match, there is a risk that the query will fail due to lack of memory. This query should only be run with interesting words that are not expected to occur often. Otherwise use `defoe.nls.queries.window_keysearch_concordance_by_date` query instead, since this one just retrieve a number of words (window) before and after each match.
