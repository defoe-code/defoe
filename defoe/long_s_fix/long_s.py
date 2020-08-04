import os
import subprocess
import re

DEFOE_PATH="/lustre/home/sc048/rosaf4/defoe/"
OS="sys-i386-64"

def longsfix_sentence(sentence):
    print("Original sentence: %s" %sentence)
    if "'" in sentence:
        sentence=sentence.replace("'", "\'\\\'\'")

    cmd = 'printf \'%s\' \''+ sentence + '\' | '+ DEFOE_PATH + 'defoe/long_s_fix/' + OS + '/lxtransduce -l spelling='+ DEFOE_PATH+ 'defoe/long_s_fix/f-to-s.lex '+ DEFOE_PATH+ 'defoe/long_s_fix/fix-spelling.gr'

    try:
        proc=subprocess.Popen(cmd.encode('utf-8'), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        if "Error" in str(stderr):
            print("---Err: '{}'".format(stderr))
            stdout_value = sentence
        else:
             stdout_value = stdout
        proc.terminate()

        fix_s= stdout_value.decode('utf-8').split('\n')[0]
    except:
        fix_s=sentence
    if re.search('[aeiou]fs', fix_s):
        fix_final=re.sub('fs', 'ss', fix_s)
    else:
        fix_final = fix_s

    print("Final sentence %s" %fix_final)
    return fix_final


sentence="This a fentence test"
longsfix_sentence(sentence)