# Identify the locations per page and geo-resolve them using the Original Edinburgh Geoparser

* It uses the Original Geoparser for identifying all posible locations within a page.
* And it also ues Edinburgh georesolve for getting the latituted and longitude of each location.
* Query module: `defoe.nls.queries.geoparser_pages.md`
* Configuration file:
  - defoe path (defoe_path)
  - operating system (os) 
  - gazetter (gazetteer)
  - Examples:
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

**Note-1**: This query is similar to the  `defoe.nls.queries.georesolution_pages`. The only difference, is that this query uses the Edinburgh geoparser for both steps: identifying locations and geo-resolve them. 

**Note-2:** Additional information about how to install and run this query, including how to install and download the Edinburgh Geoparser can be found [here](../setup-VM.md#installing-the-geoparser--georesolve-tools-inside-defoe).

