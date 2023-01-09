# SPARQL KG queries

For working **just** with RDF Knowledge Graphs. So, far we have four KG available. See bellow for details

## Knowledge Graphs: 
* [Encyclopaedia Britannica](https://zenodo.org/record/6673897)
* [ChapBooks](https://zenodo.org/record/6673995#.Yswxt5BByed) 
* [The Ladies Debating Magazine](https://zenodo.org/record/6686072#.YrNGRpDMJHZ)
* [Gazeteers of Scotland](https://zenodo.org/record/6686829#.Y7wzd-LP0rk)

## Ontologies

These RDF Knowledge Graphs have been creater with either: 

* [The ontology for the Encyclopaedia Britannica](https://francesnlp.github.io/EB-ontology/doc/index-en.html);
* Or [The ontology for the rest of the NLS collections](https://francesnlp.github.io/NLS-ontology/doc/index-en.html )

## Queries 

* frequency_keyseach_by_year: calculates the frequencies of one or several keywords or key sentences in terms definitions, applying different pre-processing techniques normalization, lemmatization, stemming. Results are grouped by year.
* publication_normalized: counts the total number of volumes, pages and words of the encyclopaedia and returns results per year.
* terms_fulltext_keysearch_by_year: searches and extracts full text definitions according different filtering settings. This query also allows us to apply different pre-processing techniques. Results are grouped by year.
* terms_snippet_keysearch_by_year: similar to the previous query, but instead returns snippets of text definitions. It allows for snippet size configuration.
* uris_keysearch: extracts URIs of terms that contain the selected keywords or key sentences in their definitions. It uses different pre-processing techniques and results are grouped by URI.

## Important


If we have a KG of a collection we have to modify the sparql_data.txt:
* http://localhost:3030/total_eb/sparql
* http://localhost:3030/chapbooks_scotland/sparql
* http://localhost:3030/ladies_debating/sparql
* http://localhost:3030/gazetters_scotlad/sparql
