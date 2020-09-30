# Identify the locations (using spaCy) per page and geo-resolve them (using the Edinburgh georesolver)

* It uses spaCy for identifying all posible locations within a page.
* It uses the Edinburgh georesolve for getting the latituted and longitude of each location.
* Query module: `defoe.nls.queries.georesolution_pages`
* Configuration file:
  - defoe path (defoe_path)
  - operating system (os) 
  - gazetter (gazetteer)
  - spaCy language model (lang_model)
  - Examples:
     - lang_model: en_core_web_lg
     - gazetteer: geonames
     - defoe_path: /home/rosa_filgueira_vicente/defoe/
     - os_type: linux
* Result format:

```
   - YEAR:
        - archive: 
        - edition: 
        - georesolution_page:
            - PLACE:
              - in-cc: 
              - lat: 
              - long: 
              - pop: 
              - snippet: 
              - type: 
              - type:

           - PLACE: 
             ....
        - lang_model: 
        - page_filename: 
        - text_unit id: 
        - title: 
```

**Note-1**: This query is similar to the  `defoe.nls.queries.geoparser_pages`. The only difference, is that this query uses spaCy for identifying the locations with a page, and just the Edinburgh gfor geo-resolve them. 

**Note-2:** Additional information about how to install and run this query, including how to install and download the Edinburgh Geoparser can be found [here](../setup-VM.md#installing-the-geoparser--georesolve-tools-inside-defoe).
