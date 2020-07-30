'''
defoe submission programme. 
From the commandline, run the following command::
    defoe-submit <type> <collection> <query> [-h] [-f inputfile]\
                                  [-r result_file] [-n num_proc] [-c config_file] [-l log_file] [...]
with parameters
:type:      simple or multiple queries
:collection:  collection to analyse
:-n num:    number of processes (optional)
:-f file:   file containing input data (required)
:-c file:   file containing configurations for the query (required)
:-r file:   file containing result file (optional)
:-l file:   log file (optional)
:-h:        print this help page
Other parameters might be required by the target mapping, for example the
number of processes if running in a parallel environment.
'''

import argparse
import os
import sys


def create_arg_parser():  # pragma: no cover
    parser = argparse.ArgumentParser(
        description='Submit a defoe workflow')
    parser.add_argument('type',  help='type of defoe query, simple or multiple')
    parser.add_argument('collection', help='collection to analyse')
    parser.add_argument('query', help='number of iterations')
    parser.add_argument('-f', '--file', metavar='input file',
                        help='file containing input dataset in TXT')
    parser.add_argument('-c', '--config_file', metavar='config file',
                        help='file containing config file in YAML')
    parser.add_argument('-r', '--result', metavar='result_file',
                        help='result_file', default="results.txt")
    parser.add_argument('-n', '--num', metavar='num_processes',
                        help='number of processes', default="1")
    parser.add_argument('-l', '--log_file', metavar='logt_file',
                        help='log_file', default="log.txt")
    return parser


def parse_common_args():   # pragma: no cover
    parser = create_arg_parser()
    return parser.parse_known_args()

def load_inputs(args):
    inputs={}
    err = 0
    inputs["collection"]=args.collection
    inputs["query"]=args.query
    if not args.file:
        err = 1
    else:
        inputs["data_file"]=args.file
        if args.config_file:
           inputs["config_file"]=args.config_file
        else:
            inputs["config_file"]=""
        inputs["result_file"]=args.result
        inputs["num_proc"] = args.num
        inputs["log_file"] = args.log_file
        if args.type == "simple":
            inputs["process_type"]= "defoe/run_query.py"
        else:
            inputs["process_type" ] ="defoe/run_queries.py"
        inputs["query_name"]="defoe."+inputs["collection"]+".queries."+inputs["query"]
    return inputs, err
        

def main():
    args, remaining = parse_common_args()
    err=0
    inputs, err =load_inputs(args)
    if err:
        print("Input file is needed: -f file containing input data")
    else:
        CMD_1="zip -r defoe.zip defoe"
        print(CMD_1)
        CMD_2="spark-submit --py-files defoe.zip "+ inputs["process_type"] + " " + inputs["data_file"]+ " " + inputs["collection"]+ " " + inputs["query_name"] + " " + inputs["config_file"] + " -r " + inputs["result_file"]  + " -n " + inputs["num_proc"] + " > "+ inputs["log_file"] 

        print(CMD_2)

if __name__ == "__main__":  # pragma: no cover
    main()
