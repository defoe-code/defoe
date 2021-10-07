"""
Query-related utility functions.
"""

from defoe import query_utils
from defoe.query_utils import PreprocessWordType, longsfix_sentence, xml_geo_entities, georesolve_cmd,  coord_xml, geomap_cmd, geoparser_cmd, geoparser_coord_xml
from nltk.corpus import words
import re
import spacy
from spacy.tokens import Doc
from spacy.vocab import Vocab
NON_AZ_REGEXP = re.compile('[^a-z]')
from nltk.corpus import words



def get_pages_matches_no_prep(title, edition, archive, filename, text, keysentences):
    """
    Get pages within a document that include one or more keywords.
    For each page that includes a specific keyword, add a tuple of
    form:

        (<TITLE>, <EDITION>, <ARCHIVE>, <FILENAME>, <TEXT>, <KEYWORD>)

    If a keyword occurs more than once on a page, there will be only
    one tuple for the page for that keyword.
    If more than one keyword occurs on a page, there will be one tuple
    per keyword.

    :return: list of tuples
    """  
    matches = []
    for keysentence in keysentences:
        sentence_match = get_sentences_list_matches(text, keysentence)
        #sentence_match_idx = get_text_keyword_idx(text, keysentence)
        if sentence_match: 
            match = (title, edition, archive, filename, text, keysentence)
            matches.append(match) 
    return matches



def get_page_matches(document,
                     keywords,
                     preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Get pages within a document that include one or more keywords.
    For each page that includes a specific keyword, add a tuple of
    form:

        (<YEAR>, <DOCUMENT>, <PAGE>, <KEYWORD>)

    If a keyword occurs more than once on a page, there will be only
    one tuple for the page for that keyword.
    If more than one keyword occurs on a page, there will be one tuple
    per keyword.

    :param document: document
    :type document: defoe.nls.document.Document
    :param keywords: keywords
    :type keywords: list(str or unicode:
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: list of tuples
    :rtype: list(tuple)
    """
    matches = []
    for keyword in keywords:
        for page in document:
            match = None
            for word in page.words:
                preprocessed_word = query_utils.preprocess_word(
                    word, preprocess_type)
                if preprocessed_word == keyword:
                    match = (document.year, document, page, keyword)
                    break
            if match:
                matches.append(match)
                continue  # move to next page
    return matches


def get_document_keywords(document,
                          keywords,
                          preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Gets list of keywords occuring within an document.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: sorted list of keywords that occur within article
    :rtype: list(str or unicode)
    """
    matches = set()
    for page in document:
        for word in page.words:
            preprocessed_word = query_utils.preprocess_word(word,
                                                            preprocess_type)
            if preprocessed_word in keywords:
                matches.add(preprocessed_word)
    return sorted(list(matches))


def document_contains_word(document,
                           keyword,
                           preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Checks if a keyword occurs within an article.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param keywords: keyword
    :type keywords: str or unicode
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: True if the article contains the word, false otherwise
    :rtype: bool
    """
    for page in document:
        for word in page.words:
            preprocessed_word = query_utils.preprocess_word(word,
                                                            preprocess_type)
            if keyword == preprocessed_word:
                return True
    return False


def calculate_words_within_dictionary(page, 
                   preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Calculates the % of page words within a dictionary and also returns the page quality (pc)
    Page words are normalized. 
    :param page: Page
    :type page: defoe.nls.page.Page
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :return: matches
    :rtype: list(str or unicode)
    """
    dictionary = words.words()
    counter= 0
    total_words= 0
    for word in page.words:
         preprocessed_word = query_utils.preprocess_word(word, preprocess_type)
         if preprocessed_word!="":
            total_words += 1
            if  preprocessed_word in dictionary:
               counter +=  1
    try:
       calculate_pc = str(counter*100/total_words)
    except:
       calculate_pc = "0" 
    return calculate_pc

def calculate_words_confidence_average(page):
    """
    Calculates the average of "words confidence (wc)"  within a page.
    Page words are normalized. 
    :param page: Page
    :type page: defoe.nls.page.Page
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :return: matches
    :rtype: list(str or unicode)
    """
    dictionary = words.words()
    counter= 0
    total_wc= 0
    for wc in page.wc:
               total_wc += float(wc)
    try:
       calculate_wc = str(total_wc/len(page.wc))
    except:
       calculate_wc = "0" 
    return calculate_wc

def get_page_as_string(page,
                          preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    Return a page as a single string.

    :param page: Page
    :type page: defoe.nls.Page
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: page words as a string
    :rtype: string or unicode
    """
    page_string = ''
    for word in page.words:
        preprocessed_word = query_utils.preprocess_word(word,
                                                         preprocess_type)
        if page_string == '':
            page_string = preprocessed_word
        else:
            page_string += (' ' + preprocessed_word)
    return page_string


def clean_text_as_string(text, flag, defoe_path, os_type):
    """
    Clean a text as a single string,
    Handling hyphenated words: combine and split and also fixing the long-s

    """
    if flag == 2:
        text_combined=text
    else:
        text_string = ''
        for word in text:
            if text_string == '':
                text_string = word 
            else:
                text_string += (' ' + word)

   
        text_separeted = text_string.split('- ')
        text_combined = ''.join(text_separeted)
   
    if (len(text_combined) > 1) and ('f' in text_combined): 
       
       text_clean = longsfix_sentence(text_combined, defoe_path, os_type) 
    else:
        text_clean= text_combined
    if flag!=2:
        text_final=text_clean.split()
    else:
        text_final=text_clean
    text_string_final = ''
    for word in text_final:
        if flag == 0 :
            if "." not in word:
                separated_str = re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', word)
            else:
                separated_str = word

            if text_string_final == '':
                 text_string_final = separated_str
            else:
                text_string_final += (' ' + separated_str)
        else:
            separated_str = re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', word)
            if text_string_final == '':
                 text_string_final = separated_str
            else:
                text_string_final += separated_str

    return text_string_final

def clean_headers_page_as_string(page):
    """
    Clean a page as a single string,
    Handling hyphenated words: combine and split and also fixing the long-s

    :param page: Page
    :type page: defoe.nls.Page
    :return: clean page words as a string
    :rtype: string or unicode
    """
    page_words=page.words
    page_string_final=clean_text_as_string(page_words, 0, defoe_path, os_type)
    header_left_words=page.header_left_words
    header_left_string_final=clean_text_as_string(header_left_words, 1, defoe_path, os_type)
    header_right_words=page.header_right_words
    header_right_string_final=clean_text_as_string(header_right_words, 1, defoe_path, os_type)
    #in case the right header is part of the text E.G. (LELAND,John,aneminentEnglishantiquarian,was)
    if len(header_right_string_final)>12:
         header_right_string_final=''
   
    #print("Header_left_string_final %s - header_right_string_final %s" %(header_left_string_final, header_right_string_final))
    return header_left_string_final, header_right_string_final, page_string_final

def filter_terms_page(page, defoe_path, os_type):
    """
    Discovering the TERMS in the leftmost side of each colum.
    :param page: Page
    :type page: defoe.nls.Page
    :return: clean page words as a string
    :rtype: string or unicode
    """
    page_words=page.words
    num_page = page.page_id
    header_left_words=page.header_left_words
    header_left=clean_text_as_string(header_left_words, 1, defoe_path, os_type)
    header_right_words=page.header_right_words
    header_right=clean_text_as_string(header_right_words, 1, defoe_path, os_type)
    #in case the right header is part of the text E.G. (LELAND,John,aneminentEnglishantiquarian,was)
    if len(header_right)>12:
         header_right=''

    type_page, header = get_header_eb(header_left, header_right)
    page_hpos_vpos_font=page.hpos_vpos_font_words
    page_term_dict={}
    page_clean_term_dict={}

   
    if len(page_hpos_vpos_font) > 1:
        if type_page == "FullPage" or type_page == "Topic":
            page_term_dict[header]=page_words
        else:
            ln = 0
            flag = 0
            while ln < len(page_hpos_vpos_font) and flag == 0:
                if len(page_hpos_vpos_font[ln]) >= 4 or ((len(page_hpos_vpos_font[ln]) == 3) and ("See" in page_hpos_vpos_font[ln][1][3])):
                    flag = 1
                elif len(page_hpos_vpos_font[ln]) == 1 and page_hpos_vpos_font[ln][0][3].isupper() and "." in page_hpos_vpos_font[ln][0][3] and len(page_hpos_vpos_font[ln][0][3])>2:
                    flag = 2  
                else:
                    ln+=1

            if flag == 2:
                header=page_hpos_vpos_font[ln][0][3].split(".")[0]
                type_page="Topic"
                page_term_dict[header]=page_words
     
            elif flag == 1:
                page_terms=[]
                num_terms = 0
                definition = []
                first_line = 1
    
                for i in range(ln, len(page_hpos_vpos_font)):
                    flag_A=0
                    if len(page_hpos_vpos_font[i]) >= 4 or ((len(page_hpos_vpos_font[i]) == 3) and ("See" in page_hpos_vpos_font[i][1][3])):

                        if (len(page_hpos_vpos_font[i]) <= 5) and (first_line == 0) and not ("See" in page_hpos_vpos_font[i][1][3]):
                                for j in range(0,len(page_hpos_vpos_font[i])):
                                    definition.append(page_hpos_vpos_font[i][j][3])

                        elif (page_hpos_vpos_font[i][0][3].isupper()) or (page_hpos_vpos_font[i][0][2]=="font7" and page_hpos_vpos_font[i][1][3].isupper()) or (first_line == 1):
                            if (first_line == 1) and not (page_hpos_vpos_font[i][0][3].isupper()) and not (page_hpos_vpos_font[i][0][2]=="font7"):
                                term="previous_page"

                            elif len(page_hpos_vpos_font[i][0][3]) <=2:
                                
                                if ("." in page_hpos_vpos_font[i][0][3]) or ("," in page_hpos_vpos_font[i][0][3] ) or ("'" in page_hpos_vpos_font[i][0][3]) or (";" in page_hpos_vpos_font[i][0][3] or (":" in page_hpos_vpos_font[i][0][3])) or ("-" in page_hpos_vpos_font[i][0][3]) or (romanNumeral(page_hpos_vpos_font[i][0][3])) or len(page_hpos_vpos_font[i][0][3])==1:
                                    if first_line == 1:
                                        term="first_article"
                                    else:
                                        flag_A=1
                                else:
                                    term=page_hpos_vpos_font[i][0][3]
                                    flag_A=0
                            else:
                                term=page_hpos_vpos_font[i][0][3]
                                if romanNumeral(term) or ("VOL." in term):
                                    flag_A = 1

                            if flag_A == 0:
                                if "," in term:
                                    new_term= term.split(",")[0]
                                elif "." in term:
                                   new_term= term.split(".")[0]
                                else:
                                    new_term = term
                                if new_term in page_term_dict:
                                    new_term= new_term+"_def"
                                if num_terms!=0:
                                    previous_term=page_terms[-1]
                                    page_term_dict[previous_term]=definition
                                definition=[]
                                page_terms.append(new_term)
                                #page_term_dict[new_term]=("", num_page)
                                page_term_dict[new_term]=""
                                num_terms+= 1
                                for j in range(1,len(page_hpos_vpos_font[i])):
                                    definition.append(page_hpos_vpos_font[i][j][3])
                            else:
                                for j in range(0,len(page_hpos_vpos_font[i])):
                                    definition.append(page_hpos_vpos_font[i][j][3])
                            
                        else:
                            for j in range(0,len(page_hpos_vpos_font[i])):
                                definition.append(page_hpos_vpos_font[i][j][3])

                    first_line = 0
    
                if len(definition)>=1:
                    if len(page_terms)>=1:    
                        previous_term=page_terms[-1]
                    else:
                        previous_term="previous_page"
                    #page_term_dict[previous_term]=(definition, num_page) 
                    page_term_dict[previous_term]=definition
                   
                if not page_term_dict:
                    page_term_dict[header]=page_words
  
    if page_term_dict:
        cont_term = 0
        num_terms = len(page_term_dict)
        for term in page_term_dict:
            clean_term=clean_text_as_string(term,2, defoe_path, os_type)
            clean_def=clean_text_as_string(page_term_dict[term],0, defoe_path, os_type)
            if cont_term + 1 == num_terms:
                last_term = 1
            else:
                last_term = 0
            if "See " in clean_def:
                related_terms= clean_def.split("See ")[1]
            elif "SEE " in clean_def:
                related_terms= clean_def.split("SEE ")[1]
            else:
                related_terms=""
          
            related_data=[]
            related_terms=related_terms.split(" ")
            for elem in related_terms:
                if elem.isupper() or "." in elem or "," in elem:
                    elem=elem.split(".")[0]
                    term=elem.split(",")[0]
                    if len(term)>2:
                        m = re.search('^([0-9]+)|([IVXLCM]+)\\.?$', term)
                        if m is None:
                            related_data.append(term.upper())
 
            page_clean_term_dict[clean_term]=(clean_def, cont_term, last_term, related_data)
            cont_term += 1
  

    if len(page_clean_term_dict)>5 and (type_page == "Topic"):
        type_page="Mix"

    return type_page, header, page_clean_term_dict, len(page_clean_term_dict)
        


def preprocess_clean_page(clean_page,
                          preprocess_type=PreprocessWordType.LEMMATIZE):


    clean_list = clean_page.split(' ') 
    page_string = ''
    for word in clean_list:
        preprocessed_word = query_utils.preprocess_word(word,
                                                         preprocess_type)
        if page_string == '':
            page_string = preprocessed_word
        else:
            page_string += (' ' + preprocessed_word)
    return page_string

def get_sentences_list_matches(text, keysentence):
    """
    Check which key-sentences from occurs within a string
    and return the list of matches.

    :param text: text
    :type text: str or unicode
    :type: list(str or uniocde)
    :return: Set of sentences
    :rtype: set(str or unicode)
    """
    match = []
    text_list= text.split()
    for sentence in keysentence:
        if len(sentence.split()) > 1:
            if sentence in text:
                count = text.count(sentence)
                for i in range(0, count):
                    match.append(sentence)
        else:
            pattern = re.compile(r'^%s$'%sentence)
            for word in text_list:
                if re.search(pattern, word):
                    match.append(sentence)
    return sorted(match)


def preprocess_clean_page_spacy(clean_page,
                          preprocess_type=PreprocessWordType.LEMMATIZE):


    clean_list = clean_page.split(' ')
    page_string = ''
    for word in clean_list:
        preprocessed_word = query_utils.preprocess_word(word,
                                                         preprocess_type)
        if page_string == '':
            page_string = preprocessed_word
        else:
            page_string += (' ' + preprocessed_word)
    return page_string


def preprocess_clean_page_spacy(clean_page):
    nlp = spacy.load('en')
    doc = nlp(clean_page)
    page_nlp_spacy=[]
    for i, word in enumerate(doc):
        word_normalized=re.sub(NON_AZ_REGEXP, '', word.text.lower())
        output="%d\t%s\t%s\t%s\t%s\t%s\t%s\t"%( i+1, word, word_normalized, word.lemma_, word.pos_, word.tag_, word.ent_type_)
        page_nlp_spacy.append(output)
    return page_nlp_spacy


def georesolve_page_2(text, lang_model):
    nlp = spacy.load(lang_model)
    doc = nlp(text)
    if doc.ents:
        flag,in_xml = xml_geo_entities(doc)
        if flag == 1:
            geo_xml=georesolve_cmd(in_xml)
            dResolved_loc= coord_xml(geo_xml)
            return dResolved_loc
        else:
           return {}
    else:
        return {}

def georesolve_page(doc):
    if doc.ents:
        flag,in_xml = xml_geo_entities(doc)
        if flag == 1:
            geo_xml=georesolve_cmd(in_xml)
            dResolved_loc= coord_xml(geo_xml)
            print(dResolved_loc)
            return dResolved_loc
        else:
           return {}
    else:
        return {}

def geoparser_page(text):
    geo_xml=geoparser_cmd(text)
    dResolved_loc= geoparser_coord_xml(geo_xml)
    return dResolved_loc



def geomap_page(doc):
    geomap_html = ''
    if doc.ents:
        flag,in_xml = xml_geo_entities(doc)
        if flag == 1:
            geomap_html=geomap_cmd(in_xml)
    #return str(geomap_html)
    return geomap_html


def get_text_keyword_idx(text,
                            keywords):
    """
    Gets a list of keywords (and their position indices) within an
    article.

    :param text: text
    :type article: string
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :return: sorted list of keywords and their indices
    :rtype: list(tuple(str or unicode, int))
    """
    text_list= text.split()
    matches = set()
    for idx, word in enumerate(text_list):
        if  word in keywords:
            match = (word, idx)
            matches.add(match)
    return sorted(list(matches))

def get_concordance(text,
                    keyword,
                    idx,
                    window):
    """
    For a given keyword (and its position in an article), return
    the concordance of words (before and after) using a window.

    :param text: text
    :type text: string 
    :param keyword: keyword
    :type keyword: str or unicode
    :param idx: keyword index (position) in list of article's words
    :type idx: int
    :window: number of words to the right and left
    :type: int
    :return: concordance
    :rtype: list(str or unicode)
    """
    text_list= text.split()
    text_size = len(text_list)

    if idx >= window:
        start_idx = idx - window
    else:
        start_idx = 0

    if idx + window >= text_size:
        end_idx = text_size
    else:
        end_idx = idx + window + 1

    concordance_words = []
    for word in text_list[start_idx:end_idx]:
        concordance_words.append(word)
    return concordance_words

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def removeNumbers(inputString):
    result=''.join(i for i in inputString if not i.isdigit())
    return result

def removeSpecialcharacters(inputString):
    return re.sub('[^A-Za-z0-9]+', '', inputString)

def splitGroups(inputString):
    match=re.match(r"([0-9]+)([A-Z]+)", inputString, re.I)
    if match:
        items = match.groups()
    else:
        items = []
    return items

def split(word): 
    return [char for char in word]

def specialCharacters(inputString):
    regex = re.compile('■@_!#$%^&*?/\|~')
    inputString_list= split(inputString)
    spc_cont=0
    for i in inputString_list:
        if re.match(r'^[_\W]+$', i):
            spc_cont+=1
    return spc_cont 
      

def hasDot(inputString):
    if "." in inputString:
        return True
    else:
        return False

def romanNumeral(inputString):
    if "." in inputString:
        word= inputString.split(".")[0]
    else:
        word = inputString
    return not set(word).difference('MDCLXVI()')

def get_header_eb(header_left, header_right):
    page_type = ''
    header = header_left + header_right
    if (header_left == '') and (header_right == ""):
        header="Empty"
        page_type="Empty"
    elif (len(header_left) <= 4) and(len(header_right) <=4):
        header= header_left+ " " + header_right
        page_type="Article"
    elif ("PREFACE" in header_left) or ("PREFACE" in header_right):
        header = "Preface"
        page_type="FullPage"
    elif "PREFACE" in header:
        header = "Preface"
        page_type="FullPage"
    elif("ENCYCLOPAEDIA" in header_left) and (len(header_right)<=4):
        header = header_right
        page_type="Article"
    elif ("Plate" in header) or ("Plafr" in header) or ("Elate" in header) or ("Tlafe" in header):
        header = "Plate"
        page_type = "FullPage"
    elif "ARTSandSCI" in header:
        header = "FrontPage"
        page_type="FullPage"
    elif "ERRATA" in header:
        header = "Errata"
        page_type="FullPage"
    elif ("LISTofAUTHORS" in header) or ("ListofAUTHORS" in header) or ("listofAuthors" in header) or ("ListOfAuthors" in header) or ("listofauthors" in header):
        header = "AuthorList"
        page_type="FullPage"

    elif ('(' in header_left) and (')' in header_right):
        header= header_left+ " " + header_right
        page_type="Article"

    elif hasNumbers(header_left) and (len(header_right)<=4) and not hasDot(header_left) and not hasDot(header_right):
        header=header_left+" " +header_right  
        page_type="Article"

    elif hasNumbers(header_right) and (len(header_left)<=4) and not hasDot(header_left) and not hasDot(header_right):
        header=header_left+" " +header_right
        page_type="Article"

    elif (('('in header_left) and (')' in header_left)) or (('C' in header_left) and (')' in header_left)):
        header=header_left
        page_type="Mix"
    elif hasDot(header_left) or hasDot(header_right):
        header_tmp= header_left + header_right
        header=header_tmp.split(".")[0]
        page_type="Topic"
    elif hasNumbers(header_right) and specialCharacters(header_right)< 3:
        header_tmp= header_left + header_right
        header=header_tmp.split(".")[0]
        page_type="Topic"
    elif hasNumbers(header_left) and specialCharacters(header_left) <3:
        header_tmp= header_left + header_right
        items=splitGroups(header_tmp)
        if items:
           header = items[1].split(".")[0]
        else:
            header = header_tmp.split(".")[0]
        page_type="Topic"
    else:
        header = header_left + header_right
        if "EncyclopaediaBritannica" in header:
            header = "EncyclopaediaBritannica"
            page_type = "Article"
        elif ("ENCYCLOPEDIA" in header) or ("THE" in header):
            header = "FrontPage" 
            page_type="FullPage"
        elif specialCharacters(header) > 5:
            page_type="FullPage"
        elif len(header) >=40:
            page_type="FullPage"
        else:
            page_type="FullPage"

    tmp_header=removeSpecialcharacters(header)
    f_header=removeNumbers(tmp_header)
    if f_header == "" :
        f_header=header
    return page_type, f_header

def get_articles_page(text, text_list, terms_view, num_words):
        articles_page={}
        latin_view=[s in words.words() for s in text_list]
        key='previous_page'
        articles_page[key]=[]
        articles_page[key].append('')
        list_key={}
        list_key[key] = 0
        half_key=''
        latin_key=''
        cont = 0
        for i in range(0, num_words):
            flag = 0
            word= text_list[i].split(",")[0]
            #term in uppercase
            #print("Studyng: %s - current key: %s, current half_key: %s, current lating_key: %s, current text in the key: %s" %(text_list[i], key, half_key, latin_key, articles_page[key]))
            if terms_view[i]:
                # UPPERCASE WITHOUT COMMA
                if ',' not in text_list[i]:
                    #ACQUIENTANDIS plegiis, - managing ACQUIETANDIS - normally uppercase in latin too.
                    # EXCLUDING N. W. of Genova  
                    #excluding II hold,
                    if (not latin_view[i]) and ('.' not in text_list[i]) and ('II' not in text_list[i]):
                        if (i< num_words -1):
                            #checking that the next one is lowe case - e.g. pleggis
                            #print("Importante: Palabra: %s, Capital de la siguiente %s, Latin de la siguiente %s" %(text_list[i], terms_view[i+1], latin_view[i+1]))
                            if (not terms_view[i+1]):
                                if (not latin_view[i+1]) or (text_list[i+1] == "de"):
                                    latin_key= latin_key + text_list[i]
                                    #print("Actualizando latin key %s" %(latin_key))
                                else:
                                    half_key = half_key + text_list[i]
                                    #print("Entro-0 a guardar half_key %s" % half_key)
                            else:
                                half_key = half_key + text_list[i]
                                #print("Entro-1 a guardar half_key %s" % half_key)

                    #See ZEUS. - managing ZEUS.
                    elif ("." in text_list[i]) and ('See' == text_list[i-1]):
                        articles_page[key][list_key[key]]= articles_page[key][list_key[key]] + ' ' + text_list[i]

                    # ABACISCUS. See ABACUS. - Managing ABACISCUS.
                    elif ("." in text_list[i]): 
                        if (i< num_words -1):
                           #ignoring Charles VIII.  
                           if (romanNumeral(text_list[i])):
                                articles_page[key][list_key[key]]= articles_page[key][list_key[key]] + ' ' + text_list[i]
                           #checking that the next one is See
                           elif ("See" == text_list[i+1]):
                               word = text_list[i].split(".")[0]
                               key = word
                               # Managing key repitions
                               if key in articles_page.keys():
                                   list_key[key] += 1
                               else:
                                   list_key[key] = 0
                                   articles_page[key]= []
                               articles_page[key].append('')
                           elif (("N." == text_list[i]) or ("S." == text_list[i]) or ("E." == text_list[i]) or ("O." == text_list[i])) and (("lat" in text_list[i+1]) or ("long" in text_list[i+1])):
                               articles_page[key][list_key[key]]= articles_page[key][list_key[key]] + ' ' + text_list[i]
                           #ignoring the header of the first page - second half
                           elif(half_key == "DCOMPLETEONARYFCIENCE"): 
                               half_key=''
                    
                           else:
                               half_key=half_key+text_list[i]

                    # AB ACO, - recording AB (of AB ACO,) 
                    else:
		           
                       half_key=half_key+text_list[i]
                       #print("Entro-2 a guardar half_key %s" % half_key)
           
                #UPPERCASE WITH COMMA     
                else:
                    if i==0:
                        key=word
                        if key in articles_page.keys():
                            list_key[key] += 1
                        else:
                            list_key[key] = 0
                            articles_page[key]= []
                        articles_page[key].append('')
                    # AATTER, or AT TER - managing TER,   
                    elif ('or' == text_list[i-1]) :
                        if half_key!='':
                            articles_page[key][list_key[key]]= articles_page[key][list_key[key]] + ' ' + half_key + ' ' + text_list[i]
                            half_key = ''
                        else:
                            articles_page[key][list_key[key]]= articles_page[key][list_key[key]] + ' ' + text_list[i]
                             #print("!Entro en - or UPPERCASE,- : key %s - text %s:" %(key, articles_page[key]))
                        #See ASTRONOMY, - managing ASTRONOMY,
                    elif ('See' == text_list[i-1]) or (romanNumeral(text_list[i])):
                        articles_page[key][list_key[key]]= articles_page[key][list_key[key]] + ' ' + text_list[i]
                    elif(i>=2): 
                        if ('or' == text_list[i-2] and terms_view[i-1]):
                            if half_key!='':
                                articles_page[key][list_key[key]]= articles_page[key][list_key[key]] + ' ' + half_key + ' ' + text_list[i]
                                half_key = ''
                            else:
                                articles_page[key][list_key[key]]= articles_page[key][list_key[key]] + ' ' + text_list[i]
                        else:
                            # AB ACO, - recording ACO, (of AB ACO,)
                            # key= ABACO,
                            if half_key!='':
                                key=half_key + word
                                half_key=''
                                flag = 1
                            else:
                                # double A, but - Avoiding to create a new key when UPPERCASE, after a but 
                                if (i < num_words -1):
                                    if text_list[i+1] == "but":
                                        articles_page[key][list_key[key]]= articles_page[key][list_key[key]] + ' ' + text_list[i] 
                                    # RECORDING THE KEY, in the normal case
                                    else:
                                        key=word
                                        flag = 1
                                # RECORDING THE KEY, in the normal case
                                else:
                                    key = word
                                    flag = 1
                            #DEALING WITH THE FIRST PAGE
                            if key == "SABAA":
                                 key=word[-2:]
                                 flag = 1
                            if flag == 1 :
                                #print(" Entro cuando encuentra nueva key: %s" % key)
                                # Managing key repitions
                                if key in articles_page.keys():
                                    list_key[key] += 1
                                else:
                                    list_key[key] = 0
                                    articles_page[key]= []
                                #Updating the articles dictionary with the new key
                                articles_page[key].append('')
                    else:
                        # AB ACO, - recording ACO, (of AB ACO,)
                        # key= ABACO,
                        if half_key!='':
                            key=half_key + word
                            half_key=''
                            flag = 1
                        else:
                            # double A, but - Avoiding to create a new key when UPPERCASE, after a but 
                            if (i < num_words -1):
                                if text_list[i+1] == "but":
                                    articles_page[key][list_key[key]]= articles_page[key][list_key[key]] + ' ' + text_list[i]
                                # RECORDING THE KEY, in the normal case
                                else:
                                    key=word
                                    flag = 1
                            # RECORDING THE KEY, in the normal case
                            else:
                                key = word
                                flag = 1
                            #DEALING WITH THE FIRST PAGE
                            if key == "SABAA":
                                key=word[-2:]
                                flag = 1
                        if flag == 1 :
                            #print(" Entro cuando encuentra nueva key: %s" % key)
                            # Managing key repitions
                            if key in articles_page.keys():
                                list_key[key] += 1
                            else:
                                list_key[key] = 0
                                articles_page[key]= []
                                #Updating the articles dictionary with the new key
                            articles_page[key].append('')

            #term in lowercase
            else:
                #UpperCase in the middle of the text
                ##ACQUIETANDIS plegiis, - managin plegiis,
                if latin_key!='':
                    if ',' in text_list[i]:
                        key=latin_key+ " " +word
                        if key in articles_page.keys():
                            list_key[key] += 1
                        else:
                            list_key[key] = 0
                            articles_page[key]= []
                        articles_page[key].append('')
                        latin_key=''
                    # ACQUIETANTIA de Jhiris et hundredh, - manaing several latin terms before the last one with comma. 
                    else:
                        latin_key= latin_key + " " + text_list[i]

                elif half_key!='':
                    if (half_key != "ANEWADICTI"):
                        articles_page[key][list_key[key]]= articles_page[key][list_key[key]] + ' ' + half_key + ' ' + text_list[i]
                        #print("Entro para darle el half_key %s al articles_page[%s]:%s" %(half_key, key, articles_page[key]))
                    half_key=''

                elif articles_page[key][list_key[key]] != '' :
                    articles_page[key][list_key[key]]= articles_page[key][list_key[key]] + ' ' + text_list[i]
                else:
                    articles_page[key][list_key[key]]= text_list[i]
        # deleting empty keys:
        empty_keys = [k for k,v in articles_page.items() if v[0] == '']
        for k in empty_keys:
            del articles_page[k]
      
        # deleting keys that are too small for being a real article:
        empty_keys =[]
        for k, v in articles_page.items():
            if (len(v[0]) < 15 ) and ("See" not in v[0]) and (len(v) == 1):
                empty_keys.append(k)
        for k in empty_keys:
            del articles_page[k]

        return articles_page
           

def get_articles_eb(header_left, header_right, text, leftmost_terms):
    type, header = get_header_eb(header_left, header_right)
    text_list= text.split()
    terms_view=[s.isupper() for s in text_list]
    num_words= len(terms_view)
    articles_page={}

    if type == "Empty" and num_words < 10:
       return type, header, articles_page, len(articles_page)
 
    elif type == "FullPage":
       articles_page[header]= [text]
       return type, header, articles_page, len(articles_page)

    elif type == "Topic":
        # We check that the page hasnt been erroneous classfied as a topic.
        if len(text_list)>=1: 
            if (terms_view[0]) and (',' in text_list[0]):
                type="Mix"
                articles_page= get_articles_page(text, text_list, terms_view, num_words)
            else:
                articles_page[header] = [text]
        return type, header, articles_page, len(articles_page)

    elif (type == "Exception"): 
        if num_words < 40 :
            type="Exception_FullPage"
            articles_page[header] = [text]

        elif ("." in header):
            type="Exception_Topic"
            articles_page[header] = [text]

        else:
            type="Exception_Article"
            articles_page= get_articles_page(text, text_list, terms_view, num_words)
        return type, header, articles_page, len(articles_page)

    elif (type == "Article") or (type == "Mix"):
        if header == "" and len(text_list)>=1:
            if ("." in text_list[0]) and (terms_view[0]):
                header=text_list[0].split(".")[0]
                type="Topic"
                articles_page[header] = [text]
            else:
                articles_page= get_articles_page(text, text_list, terms_view, num_words)

        elif num_words >= 20:
            articles_page= get_articles_page(text, text_list, terms_view, num_words)
        else:
            type="Exception_FullPage"
            articles_page["FullPage"] = [text]
 
        return type, header, articles_page, len(articles_page)
    else:
        type="Exception"
        articles_page["FullPage"] = [text]
        return type, header, articles_page, len(articles_page)
	
