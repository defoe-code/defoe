#!/usr/bin/env bash

conda install --yes lxml
conda install --yes nltk
conda install --yes pep8
conda install --yes pylint
#conda install --yes pycodestyle
conda install --yes pytest
conda install --yes PyYAML
conda install --yes regex
conda install --yes requests
conda install --yes pathlib

conda install -c conda-forge spacy
python -m spacy download en
python -m spacy download en_core_web_lg

#conda install --yes pip git
#pip install git+https://github.com/alan-turing-institute/defoe.git
