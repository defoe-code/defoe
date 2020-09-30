# Count number of articles in which appear keywords or keysentences, filtering those by target words and dates, and group by year

* Both keywords/keysentences and words in documents are cleaned (long-S and hyphen fixes) and preprocessed according to the configuration file
* Query module: `defoe.papers.queries.target_keysearch_by_year`
* Configuration file:
  - File with keywords or keysentece (data)
  - number of target words from the file with keywords/keysentences. **Note: It asumes, that the X first words/sentences of that file are the target words**
  - in which position the lexicon start. If we use 0, it means that the target words are also including in the lexicon.
  - starting year (included) from which we want to select articles.
  - ending year (included) from which we want to select articles
  - defoe path (defoe_path)
  - operating system (os) 
  - preprocessing treatment (preprocess)
  - Examples:
     - preprocess: normalize
     - data: music.txt
     - num_target: 1
     - lexicon_start: 0
     - start_year: 1918
     - end_year: 2010
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

**Note:** Use this query if you have target word(s) and date(s). Otherwise, you could use `defoe.papers.queries.keysearch_by_year` or `defoe.papers.queries.target_keysearch_by_year`.  

