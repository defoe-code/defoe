
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

# Modifying your BASHRC profile file (Optional)

Add at the end of your ~/.bashrc file the following enviroment variables

```
PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/X11/bin:$PATH
export PATH="~/miniconda3/bin:$PATH"
source /etc/environment
export SPARK_HOME=~/spark-2.4.6-bin-hadoop2.7
export JAVA_HOME="/usr/lib/jdk/jdk-10.0.2/"
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
   
For testing both tools, we have two tests available [here](https://github.com/defoe-code/defoe/tree/master/defoe/test_geoparser_scripts), that can be run just like this (after changing the *defoe_path* and *os_type* variables according to your needs):

```
cd $HOME/defoe/test_geoparser_scripts/
python geoparser_test.py
python georesolve_test.py 
```

# Dowloading some NLS Datasets

```
cd $HOME
mkdir datasets
cd datasets/
```
### Scottish Gazetteers (SG) - Size: 2.7GB

```
wget https://nlsfoundry.s3.amazonaws.com/data/nls-data-gazetteersOfScotland.zip
unzip nls-data-gazetteersOfScotland.zip "*.xml"
```

### Encyclopaedia Britannica (EB) - Size: 25GB

```
wget https://nlsfoundry.s3.amazonaws.com/data/nls-data-encyclopaediaBritannica.zip 
unizp nls-data-encyclopaediaBritannica.zip "*.xml"
```

### Creating a SG sample dataset file with one gazetteer: 

```
cd $HOME/defoe
echo /home/rosa_filgueira_vicente/datasets/nls-data-gazetteersOfScotland/97437554 > sg_sample.txt
```

# Testing Spark  

Using an Spark application (SparkPi) included in the Spark source code

```
spark-submit --class org.apache.spark.examples.SparkPi  --master local[8] --executor-memory 20G --total-executor-cores 4  $SPARK_HOME/examples/jars/spark-examples_2.11-2.4.6.jar 10
```

While the application is running, it will appear in the screen several messages being one of the last ones "Pi is roughly 3.1434151434151434". 
See bellow:

```
0/07/29 01:39:33 INFO Executor: Finished task 9.0 in stage 0.0 (TID 9). 824 bytes result sent to driver
20/07/29 01:39:33 INFO Executor: Finished task 8.0 in stage 0.0 (TID 8). 824 bytes result sent to driver
20/07/29 01:39:33 INFO TaskSetManager: Finished task 9.0 in stage 0.0 (TID 9) in 83 ms on localhost (executor driver) (9/10)
20/07/29 01:39:33 INFO TaskSetManager: Finished task 8.0 in stage 0.0 (TID 8) in 87 ms on localhost (executor driver) (10/10)
20/07/29 01:39:33 INFO TaskSchedulerImpl: Removed TaskSet 0.0, whose tasks have all completed, from pool 
20/07/29 01:39:33 INFO DAGScheduler: ResultStage 0 (reduce at SparkPi.scala:38) finished in 0.687 s
20/07/29 01:39:33 INFO DAGScheduler: Job 0 finished: reduce at SparkPi.scala:38, took 0.734743 s
Pi is roughly 3.1434151434151434
20/07/29 01:39:33 INFO SparkUI: Stopped Spark web UI at http://instance-2.us-central1-a.c.durable-primacy-284213.internal:4041
20/07/29 01:39:33 INFO MapOutputTrackerMasterEndpoint: MapOutputTrackerMasterEndpoint stopped!
20/07/29 01:39:33 INFO MemoryStore: MemoryStore cleared
20/07/29 01:39:33 INFO BlockManager: BlockManager stopped
20/07/29 01:39:33 INFO BlockManagerMaster: BlockManagerMaster stopped
20/07/29 01:39:33 INFO OutputCommitCoordinator$OutputCommitCoordinatorEndpoint: OutputCommitCoordinator stopped!
20/07/29 01:39:33 INFO SparkContext: Successfully stopped SparkContext
20/07/29 01:39:33 INFO ShutdownHookManager: Shutdown hook called
20/07/29 01:39:33 INFO ShutdownHookManager: Deleting directory /tmp/spark-21174518-da24-455d-8c97-6593f726b542
20/07/29 01:39:33 INFO ShutdownHookManager: Deleting directory /tmp/spark-98ad4407-10ed-4e28-96e8-a653055b2241
```

# Testing Defoe 

We are going to use the [nls normalize](https://github.com/defoe-code/defoe/blob/master/defoe/nls/queries/normalize.py) query, which does not need any configuration file. 

```
conda activate g-py36
cd $HOME/defoe
spark-submit --py-files defoe.zip defoe/run_query.py sg_sample.txt nls defoe.nls.queries.normalize -r results_norm_gaz -n 34
```

The result of the query will be a new file called *results_norm_gaz* inside your *defoe_path* with this information:
```
1842:
- 1
- 920
- 1129054
``` 
**NOTE**: Most of defoe queries require a configuration file (this is not the case for the normalize query), in which users indicate their operating system (either **linux** or **mac**), along with the path of their defoe installation (**defoe_path**). This is necesary for fixing the [long_S OCR](https://www.research.ed.ac.uk/portal/files/13581682/Alex_Glover_et_al_2012_Digitised_Historical_Text.pdf) errors in the collections' text (step included in most defoe queries, **but not in the normalize queries**). The [long_S fix - LINE 263](https://github.com/defoe-code/defoe/blob/master/defoe/query_utils.py) calls to a set of different scripts depending on the user's operationg system. 

The long_S fix can be tested as a single script (called long_s.py). This script is available [here](https://github.com/defoe-code/defoe/blob/master/defoe/long_s_fix/long_s.py). For running it you just need to do the following (after changing the *defoe_path* and *os_type* variables according to your needs). 

```
cd $HOME/defoe/defoe/long_s_fix/
python long_s.py
```

# Running Defoe queries

Documentation about how to run defoe queries can be found [here](https://github.com/defoe-code/defoe/blob/master/docs/run-queries.md). The most important parameters are:

```
spark-submit --py-files defoe.zip defoe/run_query.py <DATA_FILE> <MODEL_NAME> <QUERY_NAME> <QUERY_CONFIG_FILE> [-r <RESULTS_FILE>] [-e <ERRORS_FILE>] [-n <NUM_CORES>]
```

# Running Original Geoparser Defoe query

The NLS geoparser query code is [here](https://github.com/defoe-code/defoe/blob/master/defoe/nls/queries/geoparser_pages.py). To run it, we need the following steps: 

```
conda activate g-py36
cd $HOME/defoe
```
Change queries/geoparser_sg.yml with according to your needs:
```
     gazetteer: os
     bounding_box: -lb -7.54296875 54.689453125 -0.774267578125 60.8318847656 2
     defoe_path: /home/rosa_filgueira_vicente/defoe/
     os_type: linux
```
- **NOTE**: use *linux* or *macos* for indicating the type of Operating System (os_type) inside the configuration queries/geoparser_sg.yml 
       
- **IMPORTANT**: The **addfivewsnippet.xsl** stylesheet is necesary (not included in the original source code):
   - A copy of **addfivewsnippet.xsl** (and others sytlesheets) can be found at [defoe/others](https://github.com/defoe-code/defoe/blob/master/others/addfivewsnippet.xsl)
      -  Make sure that you take a copy of this *addfivewsnippet.xsl* and put it inside your *defoe_path+ geoparser-v1.1/lib/georesolve/.* . Otherwise you will get an error while running this query.


Since we are geoparsing two collections, Encyclopedia Britannica (EB) and the Scottish Gazetters (SG), we have two geoparser YML files (geoparser_sg.yml, and geoparser_eb.yml). Both files have different configurations. For EB we use *geonames* gazzeter, and for SG we use *os* gazetter plus the bounding box.

Furthermore, any future changes about *how to call to the original geoparser tool* have to be made in [geoparser_cmd function - Line 487](https://github.com/defoe-code/defoe/blob/master/defoe/query_utils.py). 

### Using the SG sample dataset (one gazetteer)

We are going to use the *sg_sample.txt* file created before. Remember that  *sg_sample.txt* needs to be placed in your *defoe_path*. 

```
zip -r defoe.zip defoe
spark-submit --py-files defoe.zip defoe/run_query.py sg_sample.txt nls defoe.nls.queries.geoparser_pages queries/geoparser_sg.yml -r geoparser_sample_results -n 34
```

### Using the SG full dataset:

- Take a copy of [sg_total.txt](https://github.com/defoe-code/defoe/blob/master/others/sg_total.txt) and modify it accorderly adding the full path to *nls-data-gazetteersOfScotland* directory. 
- Place your *sg_total.txt* inside your *defoe_path*.
- More information about how to specify data to a query can be found at [here](https://github.com/defoe-code/defoe/blob/master/docs/specify-data-to-query.md)

```
zip -r defoe.zip defoe
spark-submit --py-files defoe.zip defoe/run_query.py sg_total.txt nls defoe.nls.queries.geoparser_pages queries/geoparser_sg.yml -r geoparser_total_results -n 34
```

# Running the Georesolve Defoe query

The NLS georesolve query code is [here](https://github.com/defoe-code/defoe/blob/master/defoe/nls/queries/georesolution_pages.py). To run it, we need the following steps: 

```
conda activate g-py36
cd $HOME/defoe
```
Change queries/georesolve_sg.yml according to your needs:
```
     lang_model: en_core_web_lg
     gazetteer: os
     bounding_box: -lb -7.54296875 54.689453125 -0.774267578125 60.8318847656 2
     defoe_path: /home/rosa_filgueira_vicente/defoe/
     os_type: linux
     
```
      
- **NOTE**: use *linux* or *macos* for indicating the type of Operating System (os_type) inside the queries/georesolve_sg.yml configuration file.

Since we are georesolving two collections, Encyclopedia Britannica (EB) and the Scottish Gazetters (SG), we have two georesolve YML files (georesolve_sg.yml, and georesolve_eb.yml). Both files have different configurations. For EB we use *geonames* gazzeter, and for SG we use *os* gazetter plus the bounding box.

Furthermore, any future changes about *how to call to the georesolve tool* have to be made in [georesolve_cmd function - Line 380](https://github.com/defoe-code/defoe/blob/master/defoe/query_utils.py). 

### Using the SG sample dataset (one gazetteer):

We are going to use the *sg_sample.txt* file created before. Remember that *sg_sample.txt* needs to be placed in your *defoe_path*. 

```
zip -r defoe.zip defoe
spark-submit --py-files defoe.zip defoe/run_query.py sg_sample.txt nls defoe.nls.queries.georesolution_pages queries/georesolve_sg.yml -r georesolve_sample_results -n 34
```

### Using the SG full dataset:
- Take a copy of [sg_total.txt](https://github.com/defoe-code/defoe/blob/master/others/sg_total.txt) and modify it accorderly adding the full path to *nls-data-gazetteersOfScotland* directory. 
- Place your *sg_total.txt* inside your *defoe_path*
- More information about how to specify data to a query can be found at [here](https://github.com/defoe-code/defoe/blob/master/docs/specify-data-to-query.md) 

```
zip -r defoe.zip defoe
spark-submit --py-files defoe.zip defoe/run_query.py sg_total.txt nls defoe.nls.queries.georesolution_pages queries/georesolve_sg.yml -r georesolve_total_results -n 34
```


# QUICK TESTS: Using just one gazetteer's page

###  Creating a directory with a gazetteer with just one page. 

```
cd datasets
mkdir sg_simple_sample
cd sg_simple_sample/
mkdir 97437554
cd 97437554
cp ../../dataset/nls-data-gazetteersOfScotland/97437554/97437554-mets.xml 
mkdir alto
cd alto
cp ../../dataset/nls-data-gazetteersOfScotland/97437554/alto/97440572.34.xml
```
So, now we have a directory in datasets, called sg_simple_sample, which has justa gazetteer folder (97437554) with one ALTO page (97440572.34.xml).

### Running defoe queries with this dataset

Now, enter in your defoe path and create the datafile necessary for defoe:
```
cd $HOME/defoe
echo /home/rosa_filgueira_vicente/datasets/sg_simple_sample/97437554/ > sg_one_page.txt
zip -r defoe.zip defoe
```

#### Run the Georesolve Query:

Remember to change first the queries/georesolve_sg.yml configuration file according to your needs.
```
spark-submit --py-files defoe.zip defoe/run_query.py sg_one_page.txt nls defoe.nls.queries.georesolution_pages queries/georesolve_sg.yml -r sample_97437554_97440572.34_georesolve -n 34
```
Check your sample_97437554_97440572.34_georesolve result file with [this one](https://github.com/defoe-code/defoe/blob/master/others/sample_97437554_97440572.34_georesolve)

#### Run the Original Geoparser Query:

Remember to change first the queries/geoparser_sg.yml configuration file according to your needs.

```
spark-submit --py-files defoe.zip defoe/run_query.py sg_one_page.txt nls defoe.nls.queries.geoparser_pages queries/geoparser_sg.yml -r sample_97437554_97440572.34_orig_geoparser -n 34
```

Check your sample_97437554_97440572.34_orig_geoparser result file with [this one](https://github.com/defoe-code/defoe/blob/master/others/sample_97437554_97440572.34_orig_geoparser)


# Installing HADDOP (Optional)

You need to have JAVA already installed
```
wget http://mirror.vorboss.net/apache/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz
tar -xvzf hadoop-3.3.0.tar.gz 
sudo mv hadoop-3.3.0 /usr/local/hadoop
```

Checking your installation
```
mkdir ~/input
cp /usr/local/hadoop/etc/hadoop/*.xml ~/input
/usr/local/hadoop/bin/hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.0.jar grep ~/input ~/gre
p_example 'allowed[.]*'
cat ~/grep_example/*. --> Result:
22      allowed.
1       allowed
```


