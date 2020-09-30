# Get concordance (also called details) of articles in which we have keywords or keysentences and group by year

* Both keywords/keysentences and words in documents are cleaned (long-S and hyphen fixes) and preprocessed according to the configuration file
* Query module: `defoe.papers.queries.keysentence_by_year_details`
* Configuration file:
  - defoe path (defoe_path)
  - operating system (os) 
  - preprocessing treatment (preprocess)
  - File with keywords or keysentece (data)
  - Examples:
     - preprocess: normalize
     - data: music.txt
     - defoe_path: /lustre/home/sc048/rosaf4/defoe/
     - os_type: linux
* Result format:

```
          <YEAR>:
          [
            [- article_id: 
             - authors:
             - filename:
             - issue_id:
             - page_ids:
             - text:
             - term
             - title ]
            ...
          ],
          <YEAR>:
          ...

```

**Note:** Use this query if you have do not target word(s). Otherwise, you could use `defoe.papers.queries.target_keysearch_by_year_details`.  

