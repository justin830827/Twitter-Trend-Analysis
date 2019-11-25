# ADBI TOP K

Please follow below steps in order to run the application.

## Installing Project Dependencies
1. Create `CSC591_ADBI_v3` virtual machine in VCL 
2. Log in to VM
3. Create an apps folder in the root folder of VCL machine: `mkdir /apps` 
4. Download project source code and unzip it to `/apps`
5. `cd /apps/adbi-top-k`
6. `pip3 install -r requirements.txt`

## Project Configuration
We have added Twitter API keys to `config.ini`. In case these keys do not work for you. 
Feel free to update them with your own keys.


## Installing and Starting ElasticSearch on VCL
Please run the following commands to install and start ElasticSearch on VCL.
For convenience these commands have been captured in a script called `scripts/install.elastic.sh`
```
sudo apt-get --yes --assume-yes install apt-transport-https
echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list
sudo apt-get --yes --assume-yes update && sudo apt-get --yes --assume-yes --allow-unauthenticated install elasticsearch
sudo systemctl start elasticsearch.service
```

## Starting Kafka
1. Start Zookeeper by running `$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties`
2. Start Kafka by executing `$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties`

Note: for convenience these steps have been put in a script file `scripts/start.kafka.sh` which will 
launch Kafka in background and redirect their output to log files.

## Starting Application
Once you have started ElasticSearch and Kafka. Please run the following command
to start ADBI Top K application.
`python3 web_server.py`

## Collecting Data
Once ADBI Top K server is started, you will need to start ingestion and indexing of data.
We have implemented REST API to be able to start/stop these processes. By default,
the web server will start on port 5000. You will need to make sure that this port is
forwarded to your local machine in order to access the web server. Please follow one of 
the following guides to expose the ports 
* https://www.ssh.com/ssh/tunneling/example
* https://www.akadia.com/services/ssh_putty.html

Note: We were asked to forward ports for an assignment in this course and hoping that TAs and instructor can do the same. 

Once you have expose port 5000, please open the following page
http://localhost:5000/api

Below are steps that will allow you to start ingestion and indexing
1. Click on *heavyhitters*
2. Select `heavyhitters/ingestion/start`
3. Click *Try It Out*
4. Click *Execute*
5. Select `heavyhitters/indexing/start`
6. Click *Try It Out*
7. Click *Execute*

If everything is running fine, you should see ElasticSearch indexing logs saying that
data is being posted one in every few milliseconds. This log will not contain messages
themselves unless you increase log level in `logging.conf` to `DEBUG`

Please let the application ingest and index data for at least five minutes before quering for top K.

## Executing Queries
We have developed a GUI client for our application. You may access it via 
http://localhost:5000/
The interface should be intuitive. There are few gatchas though.
* Timestamp can be relative (now, now-1d/d, etc) or
* Timestamp need to follow [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format
  * Please make sure to remove timezone from the timestamp
  * This is the last five characters
  * For example: `2019-04-19T12:02:23` instead of `2019-04-19T12:02:23-0700`
  * All timestamps in the system are in UTC
* Algorithm takes from 5 to 30 minutes to execute depending on data set size
  * This can be improved by adding more Spark worker nodes

Once you submit a query, you will be able to see Spark logs in the shell where you launched the server.
Please watch our recorded demo for more details.

## Demo video
Please see the live demo video on this [link](https://www.youtube.com/watch?v=KMEO6mVOHWA&feature=youtu.be)