import os
import subprocess
import re

DEFOE_PATH="/Users/rosafilgueira/EPCC/TDM/CDS/defoe-code/defoe/"
OS="sys-i386-snow-leopard"
gazetter = "os"
bounding_box = " -lb -7.54296875, 54.689453125, -0.774267578125, 60.8318847656 2 "

def geoparser_cmd(text):
    atempt=0
    flag = 1
    geoparser_xml = ''
    if "'" in text:
        text=text.replace("'", "\'\\\'\'")

    cmd = 'echo \'%s\' \''+ text + '\' | '+ DEFOE_PATH + 'geoparser-v1.1/scripts/run -t plain -g ' + gazetter + bounding_box + ' -top | ' + DEFOE_PATH+ 'georesolve/bin/'+ OS + '/lxreplace -q s | '+ DEFOE_PATH + 'geoparser-v1.1/bin/'+ OS +'/lxt -s '+ DEFOE_PATH+'geoparser-v1.1/lib/georesolve/addfivewsnippet.xsl'

    
    
    print("CMD is %s" %cmd)

    while (len(geoparser_xml) < 5) and (atempt < 10000) and (flag == 1):
        proc=subprocess.Popen(cmd.encode('utf-8'), shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.terminate()
        stdout, stderr = proc.communicate()
        if "Error" in str(stderr):
            flag = 0
            print("err: '{}'".format(stderr))
        else:
            geoparser_xml = stdout
        atempt += 1
        print(stdout, stderr)
    print("--->Geoparser %s" %geoparser_xml)
    return geoparser_xml

sentence ="I like to live in Madrid"
geoparser_cmd(sentence)

