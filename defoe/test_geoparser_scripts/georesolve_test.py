import os
import subprocess
import re
import spacy
from spacy.tokens import Doc
from spacy.vocab import Vocab


#change this according to your path
defoe_path ="/Users/rf208/Research/NLS-Fellowship/work/defoe/"
gazetteer = "os"
os_type= "sys-i386-snow-leopard"
bounding_box = " -lb -7.57216793459 49.959999905 1.68153079591 58.6350001085 2 "

def georesolve_page_2(text):
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
    if doc.ents:
        flag,in_xml, snippet = xml_geo_entities_snippet(doc)
        if flag == 1:
            geo_xml=georesolve_cmd(in_xml)
            return geo_xml
        else:
           return {}
    else:
        return {}

def xml_geo_entities_snippet(doc):
    snippet= {}
    id=0
    xml_doc='<placenames> '
    flag=0
    index=0
    for token in doc:
        if token.ent_type_ == "LOC" or token.ent_type_ == "GPE":
            id=id+1
            toponym = token.text
            child ='<placename id="' + str(id) + '" name="' + toponym + '"/> '
            xml_doc= xml_doc+child
            flag=1
            left_index = index - 5
            if left_index <=0:
                left_index = 0

            right_index = index + 6
            if right_index >= len(doc):
                right_index = len(doc)

            left=doc[left_index:index]
            right=doc[index+1:right_index]
            snippet_er=""
            for i in left:
                snippet_er+= i.text + " "
            snippet_er+= token.text + " "
            for i in right:
                snippet_er+= i.text + " "

            snippet_id=toponym+"-"+str(id)
            snippet[snippet_id]=snippet_er
        index+=1
    xml_doc=xml_doc+ '</placenames>'
    return flag, xml_doc, snippet


def georesolve_cmd(in_xml):
    georesolve_xml =''
    atempt=0
    flag = 1
    if "'" in in_xml:
        in_xml=in_xml.replace("'", "\'\\\'\'")
   
    cmd = 'printf \'%s\' \''+ in_xml + '\' | '+ defoe_path + 'georesolve/scripts/geoground -g ' + gazetteer + ' ' + bounding_box + ' -top'
    print("CMD is %s" % cmd)  
    while (len(georesolve_xml) < 5) and (atempt < 10) and (flag == 1):
        proc=subprocess.Popen(cmd.encode('utf-8'), shell=True,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        atempt= atempt + 1
        stdout, stderr = proc.communicate()
        if "Error" in str(stderr):
            flag = 0
            print("err: '{}'".format(stderr))
            georesolve_xml =  ''
        else:
            georesolve_xml = stdout
        atempt += 1
        print(atempt,stdout, stderr)
    print("----> Georesolve %s" %georesolve_xml)
    return georesolve_xml


sentence ="I like to live in Edinburgh, which is one of the Scottish cities."
georesolve_page_2(sentence)

