import os
import subprocess
import re

defoe_path ="/home/rosa_filgueira_vicente/defoe/"
os = "sys-i386-64"
gazetteer = "os"
bounding_box = " -lb -7.54296875, 54.689453125, -0.774267578125, 60.8318847656 2 "

def geoparser_cmd(text):
    atempt = 0
    flag = 1
    geoparser_xml = ''
    if "'" in text:
        text=text.replace("'", "\'\\\'\'")

    cmd = 'echo \'%s\' \''+ text + '\' | '+ defoe_path + 'geoparser-v1.1/scripts/run -t plain -g ' + gazetteer + ' '+ bounding_box + ' -top | ' + defoe_path+ 'georesolve/bin/'+ os + '/lxreplace -q s | '+ defoe_path + 'geoparser-v1.1/bin/'+ os +'/lxt -s '+ defoe_path+'geoparser-v1.1/lib/georesolve/addfivewsnippet.xsl'

    print("CMD is %s" %cmd)

    while (len(geoparser_xml) < 5) and (atempt < 10) and (flag == 1):
        proc=subprocess.Popen(cmd.encode('utf-8'), shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if "Error" in str(stderr):
            flag = 0
            print("err: '{}'".format(stderr))
        else:
            geoparser_xml = stdout
        print(atempt, stdout, stderr)
        atempt+=1
    print("--->Geoparser %s" %geoparser_xml)
    return geoparser_xml

sentence ="I like to live in Madrid"
geoparser_cmd(sentence)

