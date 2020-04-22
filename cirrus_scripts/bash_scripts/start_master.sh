#!/bin/bash

module load anaconda/python3
source activate cirrus-py36
export SPARK_HOME=${HOME}/spark-2.4.0-bin-hadoop2.7
cd $SPARK_HOME/

sbin/start-master.sh
echo "Started spark Master $HOSTNAME"
