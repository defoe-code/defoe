
# Installing Generic Tools
- sudo apt-get install wget
- sudo apt-get install zip
- sudo apt-get install git
- sudo apt-get install python3
- sudo apt-get install pip
- wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
- ./Miniconda3-latest-Linux-x86_64.sh

# Installing Spark
- wget http://mirror.vorboss.net/apache/spark/spark-2.4.6/spark-2.4.6-bin-hadoop2.7.tgz
- tar -xvf spark-2.4.6-bin-hadoop2.7.tgz 

# Installing JAVA 10
- wget https://download.java.net/java/GA/jdk10/10.0.2/19aef61b38124481863b1413dce1855f/13/openjdk-10.0.2_linux-x64_bin.tar.gz
- tar -xvf openjdk-10.0.2_linux-x64_bin.tar.gz
- mkdir -p /usr/lib/jdk
- sudo mv jdk-10.0.2 /usr/lib/jdk
- sudo update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jdk/jdk-10.0.2/bin/javac" 1
- sudo update-alternatives --config java
- sudo update-alternatives --config javac

# Modifying your BASHRC (enviroment variables)

- PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/X11/bin:$PATH
- export PATH="~/miniconda3/bin:$PATH"
- source /etc/environment
- export SPARK_HOME=~/spark-2.4.6-bin-hadoop2.7
- export $JAVA_HOME="/usr/lib/jdk/jdk-10.0.2/"
- export PATH=$PATH:$SPARK_HOME/bin
- export PATH=$PATH:$JAVA_HOME/jre/bin

# Cloning defoe and installing its requirements 
- git clone https://github.com/defoe-code/defoe.git
- conda create -n g-py36 python=3.6 anaconda
- conda activate g-py36
- cd $HOME/defoe
- ./requirements.sh
- **zip -r defoe.zip defoe**

**Note**: Every time you change something inside defoe library, you need to **ZIP** it. 

# Installing the Geoparser + Georesolve tools inside defoe 
- wget http://homepages.inf.ed.ac.uk/grover/rosa/georesolve.tgz
- cp georesolve.tgz defoe/.
- Follow the necesary steps to download the [Edinburgh Geoparser](https://www.inf.ed.ac.uk/research/isdd/admin/package?view=1&id=187) 
- cd $HOME/defoe
- tar -zxvf geoparser-march2016.tar.gz
- tar -zxvf georesolve.tgz
- **zip -r defoe.zip defoe**

**Note**: defoe assumes that **geoparser-v1.1** and **georesolve** directories are in:
      - XXX/defoe/geoparser-v1.1
      - XXX/defoe/georesolve
   - *XXX* is the path were you clone the defoe repository (e.g. $HOME)
 
# Datasets and sg_sample.txt 
- cd $HOME
- mkdir datasets
- cd datasets/
- wget https://nlsfoundry.s3.amazonaws.com/data/nls-data-gazetteersOfScotland.zip
- unzip nls-data-gazetteersOfScotland.zip "*.xml"
- cd $HOME/defoe
- cat home/rosa_filgueira_vicente/datasets/nls-data-gazetteersOfScotland/97437554 > sg_sample.txt

# Testing Spark with an example
- $SPARK_HOME/bin/spark-submit --class org.apache.spark.examples.SparkPi  --master spark://$hostmaster:7077 --executor-memory 20G --total-executor-cores 34  $SPARK_HOME/examples/jars/spark-examples_2.11-2.4.6.jar 1000

# Testing Defoe 
- conda activate g-py36
- cd $HOME/defoe
- spark-submit --py-files defoe.zip defoe/run_query.py sg_sample.txt nls defoe.nls.queries.normalize -r results_norm_gaz -n 34

# Running Original Geoparser query
- conda activate g-py36
- cd $HOME/defoe
- change queries/geoparser.yml with according to your needs:
   - more queries/geoparser.yml 
      - gazetter: os
      - bounding_box: -lb -7.54296875, 54.689453125, -0.774267578125, 60.8318847656 2
      - defoe_path: /home/rosa_filgueira_vicente/defoe/
      - os : linux
      
- **IMPORTANT**: The file **addfivewsnippet.xsl** stylesheet it is necesary (not included in the original geoparser source code).
      - A copy of this stylesheet (and others sytlesheets) can be found in [defoe/others](https://github.com/defoe-code/defoe/blob/master/others/addfivewsnippet.xsl)
      - Make sure that you take a copy of this *addfivewsnippet.xsl* and put it inside your *defoe_path+ geoparser-v1.1/lib/georesolve/.*

- **zip -r defoe.zip defoe**
- spark-submit --py-files defoe.zip defoe/run_query.py sg_sample.txt nls defoe.nls.queries.geoparser_pages queries/geoparser.yml -r geoparser_sample_results -n 34

# Running Georesolve query
- conda activate g-py36
- cd $HOME/defoe
- change queries/georesolve.yml according to your needs:
   - more queries/georesolve.yml 
      - lang_model: en_core_web_lg
      - gazetter: os
      - bounding_box: -lb -7.54296875, 54.689453125, -0.774267578125, 60.8318847656 2
      - defoe_path: /home/rosa_filgueira_vicente/defoe/
      - os : linux
- **zip -r defoe.zip defoe**
- spark-submit --py-files defoe.zip defoe/run_query.py sg_sample.txt nls defoe.nls.queries.georesolution_pages queries/georesolve.yml -r georesolve_sample_results -n 34






