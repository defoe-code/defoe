
# Installing Generic Tools

```
sudo apt-get install wget
sudo apt-get install zip
sudo apt-get install git
sudo apt-get install python3
sudo apt-get install pip
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
```

# Installing Spark

```
wget http://mirror.vorboss.net/apache/spark/spark-2.4.6/spark-2.4.6-bin-hadoop2.7.tgz
tar -xvf spark-2.4.6-bin-hadoop2.7.tgz 
```

# Installing JAVA 10

```
wget https://download.java.net/java/GA/jdk10/10.0.2/19aef61b38124481863b1413dce1855f/13/openjdk-10.0.2_linux-x64_bin.tar.gz
tar -xvf openjdk-10.0.2_linux-x64_bin.tar.gz
mkdir -p /usr/lib/jdk
sudo mv jdk-10.0.2 /usr/lib/jdk
sudo update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jdk/jdk-10.0.2/bin/javac" 1
sudo update-alternatives --config java
sudo update-alternatives --config javac
```

# Modifying your BASHRC profile file

Add at the end of your ~/.bashrc file the following enviroment variables

```
PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/X11/bin:$PATH
export PATH="~/miniconda3/bin:$PATH"
source /etc/environment
export SPARK_HOME=~/spark-2.4.6-bin-hadoop2.7
export $JAVA_HOME="/usr/lib/jdk/jdk-10.0.2/"
export PATH=$PATH:$SPARK_HOME/bin
export PATH=$PATH:$JAVA_HOME/jre/bin
```

# Cloning Defoe and installing its requirements 

We will refer to the location in which the defoe repository has be cloned as  *defoe_path* (e.g */home/rosa_filgueira_vicente/defoe/*)

```
git clone https://github.com/defoe-code/defoe.git
conda create -n g-py36 python=3.6 anaconda
conda activate g-py36
cd $HOME/defoe
./requirements.sh
zip -r defoe.zip defoe
```

**Note**: Every time you change something inside defoe library, you need to **ZIP the DEFOE code**. If you dont change nothing, you dont need to zip it again.  

# Installing the Geoparser + Georesolve tools inside defoe 

```
wget http://homepages.inf.ed.ac.uk/grover/rosa/georesolve.tgz
cp georesolve.tgz defoe/.
```
Follow the necesary steps to download the [Edinburgh Geoparser](https://www.inf.ed.ac.uk/research/isdd/admin/package?view=1&id=187) 

```
cd $HOME/defoe
tar -zxvf geoparser-march2016.tar.gz
tar -zxvf georesolve.tgz
zip -r defoe.zip defoe
```

**Note**: defoe assumes that **geoparser-v1.1** and **georesolve** directories are inside your *defoe_path*:
   - /home/rosa_filgueira_vicente/defoe/geoparser-v1.1
   - /home/rosa_filgueira_vicente/defoe//georesolve

# Dowloading Datasets

```
cd $HOME
mkdir datasets
cd datasets/
```
### Scottish Gazetteer (2.7GB)

```
wget https://nlsfoundry.s3.amazonaws.com/data/nls-data-gazetteersOfScotland.zip
unzip nls-data-gazetteersOfScotland.zip "*.xml"
```

### Encyclopaedia Britannica (25GB)

```
wget https://nlsfoundry.s3.amazonaws.com/data/nls-data-encyclopaediaBritannica.zip 
unizp nls-data-encyclopaediaBritannica.zip "*.xml"
```

### Creating a SAMPLE dataset file with Scottish Gazetters: 

```
cd $HOME/defoe
echo /home/rosa_filgueira_vicente/datasets/nls-data-gazetteersOfScotland/97437554 > sg_sample.txt
```

# Testing Spark  

Using an Spark application (SparkPi) included in the Spark source code

```
spark-submit --class org.apache.spark.examples.SparkPi  --master spark://$hostmaster:7077 --executor-memory 20G --total-executor-cores 34  $SPARK_HOME/examples/jars/spark-examples_2.11-2.4.6.jar 1000
```

# Testing Defoe 

```
conda activate g-py36
cd $HOME/defoe
spark-submit --py-files defoe.zip defoe/run_query.py sg_sample.txt nls defoe.nls.queries.normalize -r results_norm_gaz -n 34
```
**NEW**: Most of defoe queries require a configuration file (this is not the case for the normalize query), in which users indicate their operating system (either **linux** or **mac**), along with the path of their defoe installation (**defoe_path**). This is necesary for cleaning the collections' text (step included in most defoe queries, **but not in the normalize queries**). The [cleaning step LINE #263](https://github.com/defoe-code/defoe/blob/master/defoe/query_utils.py) calls to a set of different scripts depending on the user's operationg system.  

# Running Defoe queries

Documentation about how to run defoe queries can be found [here](https://github.com/defoe-code/defoe/blob/master/docs/run-queries.md). The most important parameters are:

```
spark-submit --py-files defoe.zip defoe/run_query.py <DATA_FILE> <MODEL_NAME> <QUERY_NAME> <QUERY_CONFIG_FILE> [-r <RESULTS_FILE>] [-e <ERRORS_FILE>] [-n <NUM_CORES>]
```

# Running Original Geoparser Defoe query

```
conda activate g-py36
cd $HOME/defoe
```
Change queries/geoparser.yml with according to your needs:
```
     gazetter: os
     bounding_box: -lb -7.54296875, 54.689453125, -0.774267578125, 60.8318847656 2
     defoe_path: /home/rosa_filgueira_vicente/defoe/
     os: linux
```
- **NOTE**: use *linux* or *macos* for indicating the type of Operating System (os) inside the configuration queries/geoparser.yml 
       
- **IMPORTANT**: The **addfivewsnippet.xsl** stylesheet is necesary (not included in the original source code):
   - A copy of **addfivewsnippet.xsl** (and others sytlesheets) can be found at [defoe/others](https://github.com/defoe-code/defoe/blob/master/others/addfivewsnippet.xsl)
      -  Make sure that you take a copy of this *addfivewsnippet.xsl* and put it inside your *defoe_path+ geoparser-v1.1/lib/georesolve/.* . Otherwise you will get an error while running this query.

### Using a sample dataset

We are going to use the *sg_sample.txt* file created before. Remember that  *sg_sample.txt* needs to be placed in your *defoe_path*. 

```
zip -r defoe.zip defoe
spark-submit --py-files defoe.zip defoe/run_query.py sg_sample.txt nls defoe.nls.queries.geoparser_pages queries/geoparser.yml -r geoparser_sample_results -n 34
```

### Using the full dataset:

- Take a copy of [sg_total.txt](https://github.com/defoe-code/defoe/blob/master/others/sg_total.txt) and modify it accorderly adding the full path to *nls-data-gazetteersOfScotland* directory. 
- Place your *sg_total.txt* inside your *defoe_path*.
- More information about how to specify data to a query can be found at [here](https://github.com/defoe-code/defoe/blob/master/docs/specify-data-to-query.md)

```
zip -r defoe.zip defoe
spark-submit --py-files defoe.zip defoe/run_query.py sg_total.txt nls defoe.nls.queries.geoparser_pages queries/geoparser.yml -r geoparser_total_results -n 34
```

# Running the Georesolve Defoe query

```
conda activate g-py36
cd $HOME/defoe
```
Change queries/georesolve.yml according to your needs:
```
     lang_model: en_core_web_lg
     gazetter: os
     bounding_box: -lb -7.54296875, 54.689453125, -0.774267578125, 60.8318847656 2
     defoe_path: /home/rosa_filgueira_vicente/defoe/
     os: linux
     
```
      
- **NOTE**: use *linux* or *macos* for indicating the type of Operating System (os) inside the queries/georesolve.yml configuration file.


### Using a SAMPLE dataset:

We are going to use the *sg_sample.txt* file created before. Remember that *sg_sample.txt* needs to be placed in your *defoe_path*. 

```
zip -r defoe.zip defoe
spark-submit --py-files defoe.zip defoe/run_query.py sg_sample.txt nls defoe.nls.queries.georesolution_pages queries/georesolve.yml -r georesolve_sample_results -n 34
```

### Using the full dataset:
- Take a copy of [sg_total.txt](https://github.com/defoe-code/defoe/blob/master/others/sg_total.txt) and modify it accorderly adding the full path to *nls-data-gazetteersOfScotland* directory. 
- Place your *sg_total.txt* inside your *defoe_path*
- More information about how to specify data to a query can be found at [here](https://github.com/defoe-code/defoe/blob/master/docs/specify-data-to-query.md) 

```
zip -r defoe.zip defoe
spark-submit --py-files defoe.zip defoe/run_query.py sg_total.txt nls defoe.nls.queries.georesolution_pages queries/georesolve.yml -r georesolve_total_results -n 34
```






